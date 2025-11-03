from rest_framework import viewsets
from .models import Schedule
from .serializers import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing schedules.
    Provides list, retrieve, create, update, and delete actions.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


# (future enhancement): filter schedules by user once authentication is added
# queryset = Schedule.objects.filter(user=self.request.user)