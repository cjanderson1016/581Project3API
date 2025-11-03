# schedules/urls.py
from django.urls import path
from .views import (
    ScheduleListCreateAPIView,
    ScheduleRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('<int:pk>/', ScheduleRetrieveUpdateDestroyAPIView.as_view(), name='schedule-detail'),
]
