from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Transaction, Category, Wallet
from transactions.serializers import TransactionSerializer


TRANSACTIONS_URL = reverse('home_budget:transaction-list')


class TransactionApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_transactions_list(self):
        wal = Wallet.objects.create()
        cat = Category.objects.create(name='jedzenie')
        Transaction.objects.create(wallet=wal, title='banany', amount=8.50, type='exp', category=cat)
        Transaction.objects.create(wallet=wal, title='warzywa', amount=20, type='exp', category=cat)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('title')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_amount_negative_when_expense(self):
        wal = Wallet.objects.create()
        cat = Category.objects.create(name='jedzenie')
        exp = Transaction.objects.create(wallet=wal, title='ogórki', amount=10, type='exp', category=cat)
        inc = Transaction.objects.create(wallet=wal, title='pizza', amount=40, type='inc', category=cat)

        res = self.client.get(TRANSACTIONS_URL)

        self.assertEqual(exp.amount, -10)
        self.assertEqual(inc.amount, 40)
        self.assertEqual(str(exp), '-10 zł - ogórki')
        self.assertEqual(str(inc), '40 zł - pizza')
