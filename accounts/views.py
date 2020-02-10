from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from .models import Profile
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
