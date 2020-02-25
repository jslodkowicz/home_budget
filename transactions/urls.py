from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . import views


router = DefaultRouter()

app_name = 'home_budget'

urlpatterns = [
    path('api/transactions/', views.TransactionAPIView.as_view(), name='transaction-list'),
    path('api/wallets/', views.WalletAPIView.as_view(), name='wallet-list'),
    path('wallets/', views.WalletList.as_view(), name='wallets'),
    path('wallets/<pk>/', views.WalletDetail.as_view(), name='wallet_detail'),
    path('wallet/create/', views.WalletCreate.as_view(), name='wallet_create'),
    path('wallet/<pk>/delete/', views.WalletDelete.as_view(),
         name='wallet_delete'),
    path('wallets/<pk>/invite', views.WalletContributor.as_view(),
         name='wallet_contributors'),
    path('transactions/', views.TransactionList.as_view(),
         name='transactions'),
    path('transactions/<pk>/', views.TransactionDetail.as_view(),
         name='transaction_detail'),
    path('transaction/create/', views.TransactionCreate.as_view(),
         name='transaction_create'),
    path('transaction/<pk>/delete/', views.TransactionDelete.as_view(),
         name='transaction_delete'),
    path('transaction/<pk>/invoice', views.TransactionInvoice.as_view(),
         name='transaction_invoice'),
    path('transfer/', views.Transfer.as_view(), name='transfer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
