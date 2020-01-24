from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('transaction', views.TransactionViewSet)

app_name = 'home_budget'

urlpatterns = [
    path('', include(router.urls))
]