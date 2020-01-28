from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('transaction', views.TransactionViewSet)
router.register('wallet', views.WalletViewSet)

app_name = 'home_budget'

urlpatterns = [
    path('api/', include(router.urls)),
    path('wallets/', views.wallets_list, name='wallets'),
    path('wallet/create/', views.WalletCreate.as_view(), name='wallet_create'),
    path('wallet/<pk>/delete/', views.WalletDelete.as_view(), name='wallet_delete'),
    path('transactions/', views.transaction_list, name='transactions'),
    path('transaction/create', views.TransactionCreate.as_view(), name='transaction_create'),
    path('transaction/<pk>/delete/', views.TransactionDelete.as_view(), name='transaction_delete'),
]
