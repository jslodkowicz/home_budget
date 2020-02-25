from rest_framework import serializers

from .models import Transaction, Wallet


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize transactions"""

    class Meta:
        model = Transaction
        fields = (
            'id',
            'wallet',
            'category',
            'title',
            'amount',
            'type',
            'created'
        )


class WalletSerializer(serializers.ModelSerializer):
    """Serialize wallets"""

    class Meta:
        model = Wallet
        fields = (
            'id',
            'name',
            'balance'
        )
