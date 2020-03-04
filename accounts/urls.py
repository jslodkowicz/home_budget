from django.urls import path

from . import views


urlpatterns = [
    path('api/', views.ProfileListAPI.as_view(), name='users-list'),
    path('api/<pk>/', views.ProfileDetailAPI.as_view(),
         name='users-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<pk>/profile/', views.ProfileView.as_view(), name='profile'),
]
