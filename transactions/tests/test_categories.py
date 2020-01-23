from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Category
from transactions.serializers import CategorySerializer

CATEGORIES_URL = reverse('home_budget:category-list')


class CategoryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_transactions_list(self):
        Category.objects.create(name='jedzenie')
        Category.objects.create(name='rachunki')

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

