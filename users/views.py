from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import CustomUser
from .serializers import (
    LoginSerializer,
    UserSerializer,
)


class LoginAPIView(views.APIView):
    """
    API endpoint for user login.
    """

    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        """
        Authenticate the user and return a token.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(CustomUser, id=serializer.validated_data["user"].id)

        user_serializer = UserSerializer(user)

        auth_token, created = Token.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "auth_token": auth_token.key,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class TokenRefreshAPIView(views.APIView):
    permission_classes = [AllowAny]

    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data

        auth_token = request.data["auth_token"]

        if auth_token is None:
            return Response(
                {"detail": "No token provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = Token.objects.get(key=request.data["auth_token"]).user

        user_serializer = UserSerializer(user)

        if user_serializer is None:
            return Response(
                {"detail": "User does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        auth_token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "auth_token": auth_token.key,
                "access_token": token["access"],
                "refresh_token": token["refresh"],
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
