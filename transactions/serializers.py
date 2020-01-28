from rest_framework import serializers

from .models import Transaction, Wallet


class TransactionSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        wallet = self.validated_data['wallet']
        category = self.validated_data['category']
        title = self.validated_data['title']
        amount = self.validated_data['amount']
        if self.validated_data['type'] == 'exp':
            wallet.expense(category=category, title=title, amount=amount)
        elif self.validated_data['type'] == 'inc':
            wallet.income(category=category, title=title, amount=amount)

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
