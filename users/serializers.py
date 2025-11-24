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
        fields = ('id','full_name', 'email', 'password', 'schedule_ids', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only' : True}}

    # Hashes the user's password so they are not easily found in the database. Uses sha256, Django salts the hash automatically as well.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Handle password hashing if password is provided
        password = validated_data.pop('password', None)

        # Let the base update handle other fields (including schedule_ids)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
        
