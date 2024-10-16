from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import logging

# Set up a logger for this module
logger = logging.getLogger(__name__)


class UserRegisterView(APIView):

    permission_classes = [
        permissions.IsAdminUser
    ]  # Only admin can access this endpoint

    def post(self, request):
        # Retrieve username and password from the request data
        username = request.data.get("username")
        password = request.data.get("password")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            logger.error("Username with '%s' already exists", username)
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        logger.info("User created successfully for '%s'", username)

        # Respond with the created user's username
        return Response({"username": user.username}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to access this endpoint

    def post(self, request):
        # Retrieve username and password from the request data
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens if authentication is successful
            refresh = RefreshToken.for_user(user)
            logger.info("'%s' logged in", username)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            logger.error("Invalid credentials for '%s", username)
            # Return error if authentication fails
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
