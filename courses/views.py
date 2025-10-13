from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# View function: request --> response

# request handlers, not traditional views (something the user sees -- a template in django)

def say_hello(request):
    return HttpResponse("Hello World!")