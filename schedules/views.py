from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Schedule
from .serializers import ScheduleSerializer

# List all schedules / Create new schedule
class ScheduleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

# Retrieve / Update / Delete a schedule
class ScheduleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


# (future enhancement): filter schedules by user once authentication is added
# queryset = Schedule.objects.filter(user=self.request.user)