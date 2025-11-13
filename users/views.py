from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import *
from .models import *

User = get_user_model() 


# Class for registration of users
class RegisterViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


    # Creates a new entry in the register database. If it is not valid then raise an error
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400) #Status 400 means bad request


# Class to handle login
class LoginViewset(APIView):
    permission_classes = [permissions.AllowAny]

    # Extract out the email and password from the database
    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password')

        #checks the user's email and the password and returns True if they exist in the register database, false otherwise
        user = authenticate(request, email=email, password=password)

        if user:
            return Response({'message': 'Login successful!'}, status=200) #Status 200 means OK
        else:
            return Response({'error': 'Invalid credentials'}, status=401) # Means invalid authentication
