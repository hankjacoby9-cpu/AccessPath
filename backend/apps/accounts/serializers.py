from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "purdue_verified", "onboarding_role",
                  "onboarding_subject", "onboarding_completed"]
        read_only_fields = ["id", "email", "purdue_verified", "onboarding_completed"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class OnboardingSerializer(serializers.Serializer):
    onboarding_role = serializers.ChoiceField(choices=User.TeachingRole.choices)
    onboarding_subject = serializers.CharField(max_length=200, required=False, allow_blank=True)
    name = serializers.CharField(max_length=200, required=False, allow_blank=True)
