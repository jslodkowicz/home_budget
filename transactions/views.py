from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView,\
                                      FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,\
                                    ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseRedirect
from decimal import Decimal

from accounts.models import UserProfile
from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer
from .forms import TransferForm, TransactionForm, WalletInvitationForm
from .utils import currency_converter


class WalletListAPI(ListCreateAPIView):
    """List all wallets or create a new wallet"""

    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Wallet.objects.filter(user=self.request.user)
        return queryset


class WalletDetailAPI(RetrieveUpdateDestroyAPIView):
    """Wallet detail, allows to retrieve, update, delete an object"""

    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset


class TransactionListAPI(ListCreateAPIView):
    """List all transactions or create new transaction"""

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset


class TransactionDetailAPI(RetrieveUpdateDestroyAPIView):
    """Transaction detail, allows to retrieve, update, delete an object"""

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset


class WalletCreate(LoginRequiredMixin, CreateView):
    """Creating a new wallet"""
    model = Wallet
    fields = ['name', 'balance', 'currency']
    success_url = reverse_lazy('home_budget:wallets')

    def get_initial(self):
        self.initial.update({'user': self.request.user})
        return self.initial

    def form_valid(self, form):
        instance = form.save()
        instance.user.add(self.request.user)
        form.save()
        return super().form_valid(form)


class WalletDelete(LoginRequiredMixin, DeleteView):
    """Deleting an existing wallet"""
    model = Wallet
    success_url = reverse_lazy('home_budget:wallets')


class WalletList(LoginRequiredMixin, ListView):
    """Retrieves a list of existing user's wallets"""
    model = Wallet

    def get_queryset(self):
        return Wallet.objects.filter(user__id=self.request.user.id)


class WalletDetail(LoginRequiredMixin, DetailView):
    """Detail view of specific wallet"""
    model = Wallet
    paginate_by = 10


class WalletContributor(LoginRequiredMixin, FormView):
    """A form for inviting a wallet contributor"""
    form_class = WalletInvitationForm
    template_name = 'transactions/wallet_contributors.html'
    success_url = reverse_lazy('home_budget:wallet_detail')

    def form_valid(self, form):
        wallet = Wallet.objects.get(id=self.kwargs["pk"])
        cd = form.cleaned_data
        try:
            invited_user = UserProfile.objects.get(email=cd['invite'])
            send_mail(
                'Invitation to wallet',
                f'User {self.request.user} has invited you \
                to contribute the wallet {wallet.name}',
                'from@example.com',
                [cd['invite']],
                fail_silently=False
            )
            wallet.user.add(invited_user)
        except UserProfile.DoesNotExist:
            pass

        return HttpResponseRedirect('/wallets')


class TransactionCreate(LoginRequiredMixin, CreateView):
    """Creating a new transaction"""
    form_class = TransactionForm
    success_url = reverse_lazy('home_budget:transactions')
    template_name = 'transactions/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        instance.user.add(self.request.user)
        form.save()
        return super().form_valid(form)


class TransactionDelete(LoginRequiredMixin, DeleteView):
    """Deleting an existing transaction"""
    model = Transaction
    success_url = reverse_lazy('home_budget:transactions')


class TransactionList(LoginRequiredMixin, ListView):
    """Retrieve a list of existing user's transactions"""
    model = Transaction
    paginate_by = 10
    ordering = ['-created']

    def get_queryset(self):
        return Transaction.objects.filter(
                wallet__user__id=self.request.user.id)


class TransactionDetail(LoginRequiredMixin, UpdateView):
    """Detail view of specific transaction"""
    model = Transaction
    fields = ('invoice',)
    template_name = 'transactions/transaction_detail.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'home_budget:transaction_detail',
            kwargs={'pk': self.object.pk}
        )


class TransactionInvoice(LoginRequiredMixin, DetailView):
    """Displays an invoice attached to specific transaction"""
    model = Transaction
    template_name = 'transactions/invoice.html'


class Transfer(LoginRequiredMixin, FormView):
    """Allows user to transfer an amount from one wallet to another"""
    form_class = TransferForm
    template_name = 'transactions/transfer.html'
    success_url = 'wallets/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        cd = form.cleaned_data
        wallet_from = cd['wallet_from'].transactions.create(
            category='TRANSFER',
            title=cd['title'],
            amount=cd['amount'],
            type='EXPENSE'
        )
        if cd['wallet_from'].currency != cd['wallet_to'].currency:
            exchange_rate = currency_converter(
                cd['wallet_from'].currency,
                cd['wallet_to'].currency
            )
            value = exchange_rate[
                f"{cd['wallet_from'].currency}_{cd['wallet_to'].currency}"
            ]
            wallet_to = cd['wallet_to'].transactions.create(
                category='TRANSFER',
                title=cd['title'],
                amount=Decimal(value) * cd['amount'],
                type='INCOME'
            )
        else:
            wallet_to = cd['wallet_to'].transactions.create(
                category='TRANSFER',
                title=cd['title'],
                amount=cd['amount'],
                type='INCOME'
            )
        wallet_from.user.add(self.request.user)
        wallet_to.user.add(self.request.user)
        return HttpResponseRedirect('/wallets/')
