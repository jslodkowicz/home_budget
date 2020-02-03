from django import forms

from .models import Wallet


class TransferForm(forms.Form):
    wallet_from = forms.ModelChoiceField(
        queryset=Wallet.objects.filter(user__is_active=True),
        to_field_name='name',
        label='From',
    )
    wallet_to = forms.ModelChoiceField(
        queryset=Wallet.objects.filter(user__is_active=True),
        to_field_name='name',
        label='To',
    )
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        super().clean()

        if self.cleaned_data['wallet_from'] == self.cleaned_data['wallet_to']:
            self.errors['wallet_to'] = self.error_class([
                'Wallet From cannot be the same as Wallet To'
            ])
