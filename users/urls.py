from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewset.as_view(), name='login'),
    path('user/', GetCurrentUser.as_view(), name='user'),
    path('reset-pass/', PasswordReset.as_view(), name='reset-pass'),
]