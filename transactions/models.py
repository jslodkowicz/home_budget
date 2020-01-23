from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Transaction(models.Model):

    TRANSACTION_TYPE = (
        ('exp', 'expense'),
        ('inc', 'income'),
    )

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    category = models.ForeignKey(Category, on_delete=models.SET(None))
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.amount} zl - {self.title}'
