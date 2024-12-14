#
# from django import forms
# from datetime import date
#
# class SalesEntryForm(forms.Form):
#     UNIT_CHOICES = [
#         ('sht', 'шт'),  # Units: шт
#         ('m3', 'м3'),   # Units: м3
#     ]
#     CURRENCY_CHOICES = [
#         ('сум', 'сум'),  # Local currency
#         ('$', 'USD'),    # US Dollar
#     ]
#
#     def __init__(self, dispatcher_choices=None, client_choices=None, *args, **kwargs):
#         super(SalesEntryForm, self).__init__(*args, **kwargs)
#         if dispatcher_choices:
#             self.fields['name'].choices = dispatcher_choices
#         if client_choices:
#             self.fields['client'].choices = client_choices
#
#     name = forms.ChoiceField(
#         label='Наименование',
#         choices=[],  # Will be set dynamically in the view
#         widget=forms.Select,
#         required=True
#     )
#     client = forms.ChoiceField(
#         label='Контрагенты',
#         choices=[],  # Will be set dynamically in the view
#         widget=forms.Select,
#         required=True
#     )
#     date = forms.DateField(
#         label='Дата',
#         widget=forms.HiddenInput(),  # Hidden in the UI
#         input_formats=['%Y-%m-%d'],
#         initial=date.today  # Automatically set to today's date
#     )
#     quantity = forms.IntegerField(label='Кол-во', required=True)
#     unit = forms.ChoiceField(
#         label='Ед.изм.',
#         choices=UNIT_CHOICES,
#         widget=forms.Select,
#         required=True
#     )
#     price = forms.DecimalField(label='Цена', max_digits=10, decimal_places=2, required=True)
#     currency = forms.ChoiceField(
#         label='Валюта',
#         choices=CURRENCY_CHOICES,
#         widget=forms.Select,
#         required=True
#     )
#     total = forms.DecimalField(
#         label='Сумма',
#         max_digits=15,
#         decimal_places=2,
#         required=False,
#         widget=forms.NumberInput(attrs={'readonly': 'readonly'})
#     )
#     car_number = forms.CharField(label='Номер Машины', max_length=20, required=True)
#     rate = forms.DecimalField(label='Курс', max_digits=10, decimal_places=2, required=True)
#     total_usd = forms.DecimalField(label='Сумма $', max_digits=15, decimal_places=2, required=True)


from django import forms
from datetime import date
from django.core.exceptions import ValidationError

class SalesEntryForm(forms.Form):
    UNIT_CHOICES = [
        ('sht', 'шт'),  # Units: шт
        ('m3', 'м3'),   # Units: м3
    ]
    CURRENCY_CHOICES = [
        ('сум', 'сум'),  # Local currency
        ('$ ', 'USD'),    # US Dollar
    ]


    name = forms.ChoiceField(label='Наименование', choices=[], widget=forms.Select, required=True)
    client = forms.ChoiceField(label='Контрагенты', choices=[], widget=forms.Select, required=True)
    date = forms.DateField(label='Дата', widget=forms.HiddenInput(), initial=date.today)
    quantity = forms.IntegerField(label='Кол-во', required=True)
    unit = forms.ChoiceField(label='Ед.изм.', choices=UNIT_CHOICES, widget=forms.Select, required=True)
    price = forms.DecimalField(label='Цена', max_digits=10, decimal_places=2, required=True)
    currency = forms.ChoiceField(label='Валюта', choices=CURRENCY_CHOICES, widget=forms.Select, required=True)
    total = forms.DecimalField(
        label='Сумма',
        max_digits=15,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
    )

    car_number = forms.ChoiceField(label='Юк мошина рақами', choices=[], widget=forms.Select, required=True)
    # rate = forms.DecimalField(label='Курс', max_digits=10, decimal_places=2, required=True)
    # total_usd = forms.DecimalField(label='Сумма $', max_digits=15, decimal_places=2, required=True)

    def __init__(self, dispatcher_choices=None, client_choices=None, car_choices=None, *args, **kwargs):
        super(SalesEntryForm, self).__init__(*args, **kwargs)
        if dispatcher_choices:
            self.fields['name'].choices = dispatcher_choices
        if client_choices:
            self.fields['client'].choices = client_choices
        if car_choices:
            self.fields['car_number'].choices = car_choices


    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')

        # Calculate the total if possible
        if quantity is not None and price is not None:
            cleaned_data['total'] = quantity * price
        else:
            raise ValidationError("Both Quantity and Price are required to calculate Total.")

        return cleaned_data
