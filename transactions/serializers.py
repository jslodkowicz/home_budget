from rest_framework import serializers

from .models import Category, Transaction, Wallet


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'wallet',
            'category',
            'title',
            'amount',
            'type',
            'created'
        )


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = (
            'name',
            'balance'
        )