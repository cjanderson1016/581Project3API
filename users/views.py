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
        current_user = request.user
        # Use serializer so the shape matches what the frontend expects (includes `schedule_ids`).
        return Response(UserSerializer(current_user).data)

    def patch(self, request, *args, **kwargs):
        """Allow the authenticated user to partially update their own fields,
        including `schedule_ids`.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        full_name = request.data.get('full_name')

        if not full_name or not full_name.strip():
            return Response({"error": "Full name is required"}, status=400)

        user = request.user
        user.full_name = full_name.strip()
        user.save()

        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        })


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {"error": "Both current and new password are required"},
                status=400
            )

        user = request.user

        # Verify current password
        if not user.check_password(current_password):
            return Response(
                {"error": "Current password is incorrect"},
                status=400
            )

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"})

