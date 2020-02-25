from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile"""
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    password1 = serializers.CharField(write_only=True, source='user.password')
    password2 = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
