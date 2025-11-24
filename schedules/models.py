'''
    File: schedules/models.py
    Description: Model for Schedule
'''

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# Schedule model
class Schedule(models.Model):
    # Reference to the user who owns the schedule
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="schedules") # allow for NULL because User auth has not been implemented yet
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules") # post-user auth version


    # Metadata
    schedule_title = models.CharField(max_length=100) # user provided title capped at 100 characters
    schedule_description = models.TextField(blank=True) # user provided description


    # Many-to-many relationship with Course
    selected_courses = models.ManyToManyField("courses.Course", related_name="schedules", blank=True) # all courses sections related to the courses selected
    displayed_courses = models.ManyToManyField("courses.Course", related_name="displayed_in_schedules", blank=True) # the courses displayed when the schedule was saved

    # Tracking creation and modification times
    created_date = models.DateTimeField(auto_now_add=True) # save the date/time when the object is first created then never updates again
    last_updated_date = models.DateTimeField(auto_now=True) # updates the date/time every time .save() is called on the object


    # Optional — a field that allows schedules for the same user to be labeled as active/inactive
    is_active = models.BooleanField(default=False)


    # Optional — stores the academic term this schedule belongs to
    term = models.CharField(max_length=20, blank=True)  # e.g. "Fall 2025", "Spring 2026"


    def __str__(self):
        return f"{self.schedule_title} ({self.user.username})"


    class Meta:
        ordering = ["-last_updated_date"]
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"


# === Example of creating a schedule (to be removed once set up):


# Create a schedule for a user
# schedule = Schedule.objects.create(
#     user=request.user,
#     schedule_title="Fall 2025 Schedule",
#     schedule_description="EECS major courses only",
#     term="Fall 2025"
# )


# # Add courses to it
# course1 = Course.objects.get(class_number=40523)
# course2 = Course.objects.get(class_number=40987)
# schedule.courses.add(course1, course2)
# ===============================================================