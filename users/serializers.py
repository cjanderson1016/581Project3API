from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model() # custom user model ScheduleUser in .models

# Take data from the frontend 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','full_name', 'email', 'password')
        extra_keyword_args = {'password': {'write_only' : True}}

    # Hashes the user's password so they are not easily found in the database.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
