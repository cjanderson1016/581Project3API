# map urls to view functions

from django.urls import path, include
from . import views # so we can reference our view functions
from rest_framework.routers import DefaultRouter # import the Django REST Framework Default Router class
from .views import CourseViewSet, search_courses_grouped

router = DefaultRouter() # create an instance of the DefaultRouter class (from the Django REST Framework)
router.register(r'', CourseViewSet) # handle the "api/courses/{insert route name here}" using the CourseViewSet defined in courses/views.py

# an array of URLPattern objects
# URLconf module -- url configuration (needs to be imported into the main url configuration in project3api/urls.py)
urlpatterns = [
    path("hello/", views.say_hello), # use the path() function to create a URLPattern (redirects "api/hello" requests to the say_hello function)
    path("search-grouped/", search_courses_grouped, name="search_courses_grouped"),
    path('', include(router.urls)), # include the routes registered using the Django REST Framework "DefaultRouter" class (redirects all "api/..." to the router)
]