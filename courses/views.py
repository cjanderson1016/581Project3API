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