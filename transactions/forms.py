from django import forms

from .models import Wallet, Transaction


class TransferForm(forms.Form):
    wallet_from = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        to_field_name='name'
    )
    wallet_to = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        to_field_name='name'
    )
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
