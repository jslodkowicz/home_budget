from rest_framework import serializers

from .models import Transaction, Wallet


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
            'user',
            'name',
            'balance'
        )
