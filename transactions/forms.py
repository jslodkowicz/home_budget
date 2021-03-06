from django import forms
from .models import Wallet, Transaction


class TransferForm(forms.Form):

    wallet_from = forms.ModelChoiceField(
        queryset=None,
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['wallet_from'].queryset = Wallet.objects.filter(
                                              user=self.request.user)
        self.fields['wallet_to'].queryset = Wallet.objects.all().distinct()

    def clean(self):
        super().clean()

        if self.cleaned_data['wallet_from'] == self.cleaned_data['wallet_to']:
            self.errors['wallet_to'] = self.error_class([
                'Wallet From cannot be the same as Wallet To'
            ])


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'wallet',
            'category',
            'title',
            'amount',
            'type',
            'created',
            'invoice'
        ]
        widgets = {
            'created': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['wallet'].queryset = Wallet.objects.filter(
                                         user=self.request.user)


class WalletInvitationForm(forms.Form):
    invite = forms.EmailField()
