from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
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


class WalletList(ListView):
    model = Wallet


class TransactionCreate(CreateView):
    model = Transaction
    fields = ['wallet', 'category', 'title', 'amount', 'type']
    success_url = reverse_lazy('home_budget:transactions')


class TransactionDelete(DeleteView):
    model = Transaction
    success_url = reverse_lazy('home_budget:transactions')


class TransactionList(ListView):
    model = Transaction
