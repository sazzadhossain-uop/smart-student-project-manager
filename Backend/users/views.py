from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
def signup_view(request):
    username = request.data.get("username") or request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "Username, email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    return Response(
        {
            "message": "Signup successful",
            "user": {
                "id": user.id,
                "name": user.username,
                "username": user.username,
                "email": user.email,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response(
          {"error": "Invalid credentials"},
          status=status.HTTP_401_UNAUTHORIZED,
      )

    if not user.check_password(password):
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    tokens = get_tokens_for_user(user)

    return Response({
        "message": "Login successful",
        "access": tokens["access"],
        "refresh": tokens["refresh"],
        "user": {
            "id": user.id,
            "name": user.username,
            "username": user.username,
            "email": user.email,
        },
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    return Response({
        "id": user.id,
        "name": user.username,
        "username": user.username,
        "email": user.email,
    })