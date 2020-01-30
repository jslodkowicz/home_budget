from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from rest_framework import viewsets


from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletCreate(CreateView):
    model = Wallet
    fields = ['user', 'name', 'balance']
    success_url = reverse_lazy('home_budget:wallets')


class WalletDelete(DeleteView):
    model = Wallet
    success_url = reverse_lazy('home_budget:wallets')


def wallets_list(request):
    wallets = Wallet.objects.all()
    return render(request, 'transactions/wallets_list.html', {'wallets': wallets})
