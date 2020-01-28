from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Transaction, Wallet
from transactions.serializers import TransactionSerializer, WalletSerializer


TRANSACTIONS_URL = reverse('home_budget:transaction-list')
WALLET_URL = reverse('home_budget:wallet-list')


class WalletApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_wallet_list(self):
        user = User.objects.create_user('jan', password='123')
        Wallet.objects.create(user=user)
        Wallet.objects.create(user=user, name='portfel')

        res = self.client.get(WALLET_URL)

        wallets = Wallet.objects.all().order_by('name')
        serializer = WalletSerializer(wallets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)


class TransactionApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('jan', password='123')

    def test_retrieve_transactions_list(self):
        wal = Wallet.objects.create(user=self.user)
        Transaction.objects.create(wallet=wal, title='banany', amount=8.50, type='exp', category='food')
        Transaction.objects.create(wallet=wal, title='warzywa', amount=20, type='exp', category='food')

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('title')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_transfer_between_wallets(self):
        wal1 = Wallet.objects.create(user=self.user, balance=6000)
        wal2 = Wallet.objects.create(user=self.user, name='Savings', balance=100000)

        wal1.transfer(wal2, 1000)

        self.assertEqual(wal1.balance, 5000)
        self.assertEqual(wal2.balance, 101000)

    def test_expense(self):
        wallet = Wallet.objects.create(user=self.user, balance=600)
        wallet.expense(category='bills', title='telefon', amount=120.5)
        self.assertEqual(wallet.balance, 479.5)
        wallet.expense(category='food', title='pizza', amount=79.5)
        self.assertEqual(wallet.balance, 400)
        wallet.expense(category='bills', title='flat', amount=1000)
        self.assertEqual(wallet.balance, -600)

    def test_income(self):
        wallet = Wallet.objects.create(user=self.user, balance=-100)
        wallet.income(category='income', title='zwrot', amount=100)
        self.assertEqual(wallet.balance, 0)
        wallet.income(category='income', title='wypłata', amount=10000)
        self.assertEqual(wallet.balance, 10000)