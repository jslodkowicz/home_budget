from django import forms

from .models import Wallet


class TransferForm(forms.Form):
    wallet_from = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        to_field_name='name',
        label='From'
    )
    wallet_to = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        to_field_name='name',
        label='To'
    )
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
