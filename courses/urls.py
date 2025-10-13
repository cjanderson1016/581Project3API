# map urls to view functions

from django.urls import path
from . import views # so we can reference our view functions

# an array of URLPattern objects
# URLconf module -- url configuration (needs to be imported into the main url configuration in project3api/urls.py)
urlpatterns = [
    path("hello/", views.say_hello) # use the path() function to create a URLPattern
]