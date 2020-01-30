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

    def test_expense(self):
        wallet = Wallet.objects.create(user=self.user, balance=600)
        payload = {
            'wallet': wallet.id,
            'title': 'banany',
            'amount': 12.30,
            'type': 'exp',
            'category': 'food'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        wallet.refresh_from_db()
        self.assertEqual(float(wallet.balance), 587.70)

    def test_income(self):
        wallet = Wallet.objects.create(user=self.user, balance=600)
        payload = {
            'wallet': wallet.id,
            'title': 'banany',
            'amount': 12.30,
            'type': 'inc',
            'category': 'food'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        wallet.refresh_from_db()
        self.assertEqual(float(wallet.balance), 612.30)
