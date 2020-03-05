from django.utils import timezone
from django.db import models

from .enums import (
    TransactionTypes,
    TransactionCategories,
    Currency
)


class Wallet(models.Model):
    """Model for storing wallets"""
    name = models.CharField(
        max_length=100,
        unique=True
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    currency = models.CharField(
        max_length=50,
        choices=Currency.choices()
    )

    def __str__(self) -> str:
        return f'{self.name} ({self.balance} {self.currency})'


class Transaction(models.Model):
    """Model for storing individual transactions"""
    wallet = models.ForeignKey(Wallet, related_name='transactions',
                               on_delete=models.CASCADE)
    category = models.CharField(max_length=50,
                                choices=TransactionCategories.choices())
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=TransactionTypes.choices())
    created = models.DateField(default=timezone.localdate)
    invoice = models.ImageField(upload_to='invoices/', blank=True)

    def save(self, *args, **kwargs) -> None:
        """A new transaction updates its wallet balance"""
        if not self.id:
            if self.type == 'EXPENSE':
                super().save(*args, **kwargs)
                self.wallet.balance -= self.amount
                self.wallet.save()
            else:
                super().save(*args, **kwargs)
                self.wallet.balance += self.amount
                self.wallet.save()
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """A deleted transaction updates its wallet balance"""
        if self.type == 'EXPENSE':
            super().delete(*args, **kwargs)
            self.wallet.balance += self.amount
            self.wallet.save()
        else:
            super().delete(*args, **kwargs)
            self.wallet.balance -= self.amount
            self.wallet.save()

    def __str__(self) -> str:
        if self.type == 'EXPENSE':
            return f'-{self.amount} zł - {self.title}'
        return f'{self.amount} zł - {self.title}'
