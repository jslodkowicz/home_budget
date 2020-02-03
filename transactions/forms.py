from django import forms

from .models import Wallet


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

    def clean(self):

        super().clean()

        wallet1 = self.cleaned_data['wallet_from']
        wallet2 = self.cleaned_data['wallet_to']

        if wallet1 == wallet2:
            self.errors['wallet_to'] = self.error_class([
                'Wallet From cannot be the same as Wallet To'
            ])