from django.db import models

# Create your models here.

# Where we define model classes that are used to pull out data from the database and present to the user

# The Course model should store the course:
#   name; code; department; credits; days; start time; end time; and instructor
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, blank=True)
    credits = models.PositiveIntegerField(default=3)
    days = models.JSONField()  # e.g. ["Mon", "Wed", "Fri"]
    start_time = models.TimeField()
    end_time = models.TimeField()
    instructor = models.CharField(max_length=100, blank=True)

    # string representation of a Course is its code and name separated by a " - "
    def __str__(self):
        return f"{self.code} - {self.name}"
