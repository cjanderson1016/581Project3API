from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# View function: request --> response

# request handlers, not traditional views (something the user sees -- a template in django)

# "Hello World" ahh view function
def say_hello(request):
    return HttpResponse("Hello World!")

# ================================================================ #
# =========== Begin views using Django REST Framework ============ #

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["subject", "course_number", "location", "type"]
    search_fields = [
        "subject",
        "course_number",
        "title",
        "topic",
        "instructor",
    ]
    ordering_fields = ["subject", "course_number", "title"]
    ordering = ["subject", "course_number"]

# The above gives us:

# | HTTP Method | URL                  | Action            |
# | ----------- | -------------------- | ----------------- |
# | GET         | `/api/courses/`      | List all courses  |
# | POST        | `/api/courses/`      | Create new course |
# | GET         | `/api/courses/<id>/` | Retrieve course   |
# | PUT/PATCH   | `/api/courses/<id>/` | Update            |
# | DELETE      | `/api/courses/<id>/` | Delete            |

# As well as filtering:

# /api/courses/?search=EECS → returns all courses where subject, title, topic, or instructor contain “EECS”
# /api/courses/?search=python → returns courses with “python” in the title or topic
# /api/courses/?subject=EECS → exact filter by subject
# /api/courses/?ordering=title → sort alphabetically by title

from django.http import JsonResponse
from django.db import models
from .models import Course

# Required component types per course (extend as needed)
REQUIRED_TYPES = {
    ("EECS", 168): ["LEC", "LBN"],  
    # add more here later
}


def has_required_type_pairs(subject, course_number, sections):
    required = REQUIRED_TYPES.get((subject, course_number))
    if not required:
        return True  # if no rule defined, accept the course

    found_types = {s["type"] for s in sections}
    return all(req in found_types for req in required)


def search_courses_grouped(request):
    """
    Custom search endpoint that:
    - groups by (subject, course_number)
    - returns all sections for each course
    - filters out invalid pairings (e.g., missing LAB)
    """
    query = request.GET.get("q", "")

    if not query:
        return JsonResponse([], safe=False)

    # match subject, course_number, or title
    sections = Course.objects.filter(
        models.Q(subject__icontains=query) |
        models.Q(course_number__icontains=query) |
        models.Q(title__icontains=query)
    )

    grouped = {}

    # group results by subject + course_number
    for sec in sections:
        key = (sec.subject, sec.course_number)
        if key not in grouped:
            grouped[key] = {
                "subject": sec.subject,
                "course_number": sec.course_number,
                "title": sec.title,
                "sections": []
            }

        grouped[key]["sections"].append({
            "id": sec.id,
            "type": sec.type,
            "days": sec.days,
            "start_time": sec.start_time,
            "end_time": sec.end_time,
            "class_number": sec.class_number,
            "instructor": sec.instructor,
        })

    # filter out groups missing required LEC/LAB pairs
    filtered_results = []
    for (subject, course_number), data in grouped.items():
        if has_required_type_pairs(subject, course_number, data["sections"]):
            filtered_results.append(data)

    return JsonResponse(filtered_results, safe=False)
