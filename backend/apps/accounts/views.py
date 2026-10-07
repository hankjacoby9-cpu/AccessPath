from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializer, OnboardingSerializer, UserSerializer


@extend_schema(request=LoginSerializer, responses=UserSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    data = LoginSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    user = authenticate(request, email=data.validated_data["email"].lower(),
                        password=data.validated_data["password"])
    if user is None:
        return Response({"detail": "Email or password is wrong."}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response(UserSerializer(user).data)


@extend_schema(request=None, responses={204: None})
@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses=UserSerializer)
@api_view(["GET"])
def me_view(request):
    return Response(UserSerializer(request.user).data)


@extend_schema(request=OnboardingSerializer, responses=UserSerializer)
@api_view(["POST"])
def onboarding_view(request):
    data = OnboardingSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    user = request.user
    for field, value in data.validated_data.items():
        setattr(user, field, value)
    user.onboarding_completed = True
    user.save()
    return Response(UserSerializer(user).data)
