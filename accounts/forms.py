from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class SignUpForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = [
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class LoginForm(AuthenticationForm):

    class Meta:
        model = UserProfile
        fields = [
            'email',
            'password',
        ]
