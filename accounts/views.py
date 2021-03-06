from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveUpdateDestroyAPIView,\
                                    ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import UserProfile
from .forms import SignUpForm
from .serializers import ProfileSerializer


class ProfileListAPI(ListCreateAPIView):
    """List all users or create a new user"""

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class ProfileDetailAPI(RetrieveUpdateDestroyAPIView):
    """User detail, allows to retrieve, update, delete an object"""

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
