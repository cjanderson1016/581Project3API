from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model() # custom user model ScheduleUser in .models

class LoginSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    is_superuser= serializers.BooleanField()
    is_staff = serializers.BooleanField()

# Take data from the frontend 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','full_name', 'email', 'password')
        extra_keyword_args = {'password': {'write_only' : True}}

    # Hashes the user's password so they are not easily found in the database. Uses sha256, Django salts the hash automatically as well.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
