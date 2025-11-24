from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import *
from .models import *

from knox.models import AuthToken # type: ignore

User = get_user_model() 

class PasswordReset(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"success": "Password updated successfully"})


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
    serializer_class = LoginSerializer
    
    # Extract out the email and password from the database
    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password')

        #checks the user's email and the password and returns True if they exist in the register database, false otherwise
        user = authenticate(request, email=email, password=password)

        if user:
            _, token=AuthToken.objects.create(user) # create a Token for the user in this session.
            return Response({ "user": self.serializer_class(user).data, "token": token})
        else:
            return Response({'error': 'Invalid credentials'}, status=401) # Means invalid authentication
        

class GetCurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user=request.user
        return Response(
            {
                "id": current_user.id,
                "email":current_user.email,
                "full_name": current_user.full_name,
                "is_staff": current_user.is_staff,
                "is_superuser": current_user.is_superuser,
            }
        )

