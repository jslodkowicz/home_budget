from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Wallet
from transactions.serializers import WalletSerializer

WALLET_URL = reverse('home_budget:wallet-list')


class WalletApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_wallet_list(self):
        Wallet.objects.create()
        Wallet.objects.create(name='portfel')

        res = self.client.get(WALLET_URL)

        wallets = Wallet.objects.all().order_by('name')
        serializer = WalletSerializer(wallets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
