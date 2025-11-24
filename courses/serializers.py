'''
    File: courses/serializers.py
    Description: Serializer for Course model
'''

# Serializers convert between model instances and JSON to work with the frontend
# Serializers define the API representation

from rest_framework import serializers
from .models import Course

# "ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes" -- Django REST Framework Documetation
# They automatically determine a set of fields and create simple default implementations for the create() and update() methods
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
