from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets
from django.http import HttpResponseRedirect

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer
from .forms import TransferForm, TransactionForm


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletCreate(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ['user', 'name', 'balance']
    success_url = reverse_lazy('home_budget:wallets')


class WalletDelete(LoginRequiredMixin, DeleteView):
    model = Wallet
    success_url = reverse_lazy('home_budget:wallets')


class WalletList(LoginRequiredMixin, ListView):
    model = Wallet

    def get_queryset(self):
        return Wallet.objects.filter(user_id=self.request.user.id)


class WalletDetail(LoginRequiredMixin, DetailView):
    model = Wallet


class TransactionCreate(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    success_url = reverse_lazy('home_budget:transactions')
    template_name = 'transactions/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('home_budget:transactions')


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    paginate_by = 10
    ordering = ['-created']

    def get_queryset(self):
        return Transaction.objects.filter(
                wallet__user__id=self.request.user.id)


class TransactionDetail(LoginRequiredMixin, DetailView):
    model = Transaction


class Transfer(LoginRequiredMixin, FormView):
    form_class = TransferForm
    template_name = 'transactions/transfer.html'
    success_url = 'wallets/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

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
