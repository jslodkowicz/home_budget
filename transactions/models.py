from django.db import models
from django.contrib.auth.models import User

from .enums import TransactionTypes, TransactionCategories


class Wallet(models.Model):
    user = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Default')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.name} ({self.balance} zł)'


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=TransactionCategories.choices())
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=TransactionTypes.choices())
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.type == 'EXPENSE':
            self.wallet.balance -= self.amount
            self.wallet.save()
        else:
            self.wallet.balance += self.amount
            self.wallet.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.type == 'EXPENSE':
            self.wallet.balance += self.amount
            self.wallet.save()
        else:
            self.wallet.balance -= self.amount
            self.wallet.save()
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        if self.type == 'exp':
            return f'-{self.amount} zł - {self.title}'
        return f'{self.amount} zł - {self.title}'
