from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Wallet(models.Model):
    name = models.CharField(max_length=100, default='Default')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.name} wallet'


class Transaction(models.Model):

    TRANSACTION_TYPE = (
        ('exp', 'expense'),
        ('inc', 'income'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET(None))
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.amount} zł - {self.title}'

    def save(self, *args, **kwargs):
        if self.type == 'exp':
            self.amount = -abs(self.amount)
        super(Transaction, self).save(*args, **kwargs)
