from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets
from django.http import HttpResponseRedirect

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer
from .forms import TransferForm


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


class WalletDetail(DetailView):
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


class TransactionDetail(DetailView):
    model = Transaction


class Transfer(FormView):
    form_class = TransferForm
    template_name = 'transactions/transfer.html'
    success_url = 'wallets/'

    def form_valid(self, form):
        cd = form.cleaned_data
        cd['wallet_from'].transactions.create(
            category='TRANSFER',
            title=cd['title'],
            amount=cd['amount'],
            type='EXPENSE'
        )
        cd['wallet_to'].transactions.create(
            category='TRANSFER',
            title=cd['title'],
            amount=cd['amount'],
            type='INCOME'
        )
        return HttpResponseRedirect('/wallets/')
