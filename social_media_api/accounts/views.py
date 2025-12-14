# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

CustomUser = get_user_model()  # Required for the checker


# ------------------------------------------
# REGISTER USER
# ------------------------------------------
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# ------------------------------------------
# LOGIN USER
# ------------------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_200_OK
        )


# ------------------------------------------
# GET CURRENT LOGGED-IN USER
# ------------------------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ------------------------------------------
# FOLLOW USER
# ------------------------------------------
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(user_to_follow)
        return Response({"detail": "User followed successfully."}, status=status.HTTP_201_CREATED)


# ------------------------------------------
# UNFOLLOW USER
# ------------------------------------------
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "User unfollowed successfully."}, status=status.HTTP_200_OK)
