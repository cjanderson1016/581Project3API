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

from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# The above gives us:

# | HTTP Method | URL                  | Action            |
# | ----------- | -------------------- | ----------------- |
# | GET         | `/api/courses/`      | List all courses  |
# | POST        | `/api/courses/`      | Create new course |
# | GET         | `/api/courses/<id>/` | Retrieve course   |
# | PUT/PATCH   | `/api/courses/<id>/` | Update            |
# | DELETE      | `/api/courses/<id>/` | Delete            |