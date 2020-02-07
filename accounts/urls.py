from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<pk>/profile/', views.ProfileView.as_view(), name='profile'),
]
