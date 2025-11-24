# schedules/serializers.py
from rest_framework import serializers
from .models import Schedule
from courses.models import Course
from courses.serializers import CourseSerializer  # For nested read-only display


# Nested Serializer for Course (in case only a small subset of fields should be returned)
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = [
#             "id",
#             "subject",
#             "course_number",
#             "title",
#             "instructor",
#             "start_time",
#             "end_time",
#             "days",
#             "location",
#             "room",
#         ]

class ScheduleSerializer(serializers.ModelSerializer):
    # Nested read-only courses for display
    displayed_courses = CourseSerializer(many=True, read_only=True)
    selected_courses = CourseSerializer(many=True, read_only=True)

    # For write operations: accept lists of course IDs mapped to model fields
    displayed_course_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        write_only=True,
        source='displayed_courses'
    )

    selected_course_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        write_only=True,
        source='selected_courses'
    )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "schedule_title",
            "schedule_description",
            "term",
            "is_active",
            "created_date",
            "last_updated_date",
            "selected_courses",
            "selected_course_ids",
            "displayed_courses",
            "displayed_course_ids",
        ]
