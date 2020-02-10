from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets
from django.http import HttpResponseRedirect

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer
from .forms import TransferForm, TransactionForm, WalletInvitationForm


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletCreate(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ['name', 'balance']
    success_url = reverse_lazy('home_budget:wallets')

    def form_valid(self, form):
        instance = form.save()
        instance.profile.add(self.request.user.profile)
        form.save()
        return super().form_valid(form)


class WalletDelete(LoginRequiredMixin, DeleteView):
    model = Wallet
    success_url = reverse_lazy('home_budget:wallets')


class WalletList(LoginRequiredMixin, ListView):
    model = Wallet

    def get_queryset(self):
        return Wallet.objects.filter(profile__user_id=self.request.user.id)


class WalletDetail(LoginRequiredMixin, DetailView):
    model = Wallet


class WalletContributor(LoginRequiredMixin, FormView):
    form_class = WalletInvitationForm
    template_name = 'transactions/wallet_contributors.html'
    success_url = reverse_lazy('home_budget:wallet_detail')

    def form_valid(self, form):
        wallet = Wallet.objects.get(id=self.kwargs["pk"])
        cd = form.cleaned_data
        try:
            invited_user = User.objects.get(email=cd['invite'])
            send_mail(
                'Invitation to wallet',
                f'User {self.request.user} has invited you to contribute the wallet {wallet.name}',
                'from@example.com',
                [cd['invite']],
                fail_silently=False
            )
            wallet.profile.add(invited_user.profile)
        except User.DoesNotExist:
            pass

        return HttpResponseRedirect('/wallets')


class WalletContributorDelete(LoginRequiredMixin, FormView):
    pass


class TransactionCreate(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    success_url = reverse_lazy('home_budget:transactions')
    template_name = 'transactions/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        instance.profile.add(self.request.user.profile)
        form.save()
        return super().form_valid(form)


class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('home_budget:transactions')


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    paginate_by = 10
    ordering = ['-created']

    def get_queryset(self):
        return Transaction.objects.filter(
                wallet__profile__user_id=self.request.user.id)


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
