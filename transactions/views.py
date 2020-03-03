from django.urls import reverse_lazy
from django.contrib.auth.models import User
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

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer
from .forms import TransferForm, TransactionForm, WalletInvitationForm


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
    model = Wallet
    fields = ['name', 'balance']
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
    model = Wallet
    success_url = reverse_lazy('home_budget:wallets')


class WalletList(LoginRequiredMixin, ListView):
    model = Wallet

    def get_queryset(self):
        return Wallet.objects.filter(user__id=self.request.user.id)


class WalletDetail(LoginRequiredMixin, DetailView):
    model = Wallet
    paginate_by = 10


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
                f'User {self.request.user} has invited you \
                to contribute the wallet {wallet.name}',
                'from@example.com',
                [cd['invite']],
                fail_silently=False
            )
            wallet.user.add(invited_user)
        except User.DoesNotExist:
            pass

        return HttpResponseRedirect('/wallets')


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
        instance.user.add(self.request.user)
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
                wallet__user__id=self.request.user.id)


class TransactionDetail(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ('invoice',)
    template_name = 'transactions/transaction_detail.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home_budget:transaction_detail',
                            kwargs={'pk': self.object.pk})


class TransactionInvoice(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/invoice.html'


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
        a = cd['wallet_from'].transactions.create(
            category='TRANSFER',
            title=cd['title'],
            amount=cd['amount'],
            type='EXPENSE'
        )
        b = cd['wallet_to'].transactions.create(
            category='TRANSFER',
            title=cd['title'],
            amount=cd['amount'],
            type='INCOME'
        )
        a.user.add(self.request.user)
        b.user.add(self.request.user)
        return HttpResponseRedirect('/wallets/')
