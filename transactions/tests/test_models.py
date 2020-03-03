from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import UserProfile
from transactions.models import Transaction, Wallet
from transactions.serializers import TransactionSerializer


TRANSACTIONS_URL = reverse('home_budget:transaction-list')
WALLET_URL = reverse('home_budget:wallet-list')


class NonAuthWalletApiTests(TestCase):
    """Test for access to Wallet data by unauthenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='test@user.com',
                                                    first_name='test',
                                                    last_name='user',
                                                    password='123')

    def test_retrieve_wallet_list_not_authenticated(self):
        """Test if not authenticated user is able to access wallet list"""
        w1 = Wallet.objects.create(name="First")
        w2 = Wallet.objects.create(name='Second')
        w1.user.add(self.user)
        w2.user.add(self.user)

        res = self.client.get(WALLET_URL)
        exp_res = {'detail': 'Authentication credentials were not provided.'}

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.json(), exp_res)


class AuthWalletApiTests(TestCase):
    """Test for displaying Wallet data by authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='test@user.com',
                                                    first_name='test',
                                                    last_name='user',
                                                    password='123')
        self.client.force_authenticate(self.user)

    def test_retrieve_wallet_list(self):
        """Test if authenticated user can see a wallet list
        associated to his account"""
        w1 = Wallet.objects.create(name="First")
        w2 = Wallet.objects.create(name='Second')
        w1.user.add(self.user)
        w2.user.add(self.user)

        res = self.client.get(WALLET_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.json()[0],
                         {'id': 1, 'name': 'First', 'balance': '0.00'})
        self.assertEqual(res.json()[1],
                         {'id': 2, 'name': 'Second', 'balance': '0.00'})


class NonAuthTransactionApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='test@user.com',
                                                    first_name='test',
                                                    last_name='user',
                                                    password='123')

    def test_retrieve_transaction_list_not_authenticated(self):
        """Test if not authenticated user is able to access transaction list"""
        w = Wallet.objects.create(name="First", balance=1000)
        w.user.add(self.user)
        t1 = Transaction.objects.create(wallet=w,
                                        title='banany',
                                        amount=8.50,
                                        type='exp',
                                        category='food')
        t2 = Transaction.objects.create(wallet=w,
                                        title='ogórki',
                                        amount=20.30,
                                        type='exp',
                                        category='food')
        t1.user.add(self.user)
        t2.user.add(self.user)

        res = self.client.get(WALLET_URL)
        exp_res = {'detail': 'Authentication credentials were not provided.'}

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.json(), exp_res)


class AuthTransactionApiTests(TestCase):
    """Test for displaying Transaction data by authenticated user"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='test@user.com',
                                                    first_name='test',
                                                    last_name='user',
                                                    password='123')
        self.client.force_authenticate(self.user)
        self.wallet = Wallet.objects.create(name='First', balance=1000)

    def test_retrieve_transactions_list(self):
        """Test if authenticated user can retrieve a transaction list"""
        t1 = Transaction.objects.create(wallet=self.wallet,
                                        title='banany',
                                        amount=8.50,
                                        type='exp',
                                        category='food')
        t2 = Transaction.objects.create(wallet=self.wallet,
                                        title='warzywa',
                                        amount=20,
                                        type='exp',
                                        category='food')
        t1.user.add(self.user)
        t2.user.add(self.user)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('title')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.json(), serializer.data)

    def test_expense(self):
        payload = {
            'wallet': self.wallet.id,
            'title': 'banany',
            'amount': 12.30,
            'type': 'EXPENSE',
            'category': 'FOOD'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 987.70)

    def test_income(self):
        payload = {
            'wallet': self.wallet.id,
            'title': 'banany',
            'amount': 12.30,
            'type': 'INCOME',
            'category': 'FOOD'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 1012.30)
