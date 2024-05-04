# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput



class CreateUserForm(UserCreationForm):
    #email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    # email = forms.EmailField(label='Email')
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


    #TESTING DATA......
# forms.py

from django import forms
from .models import CreditCard, Transaction

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_number', 'expiry_date', 'cvv', 'card_name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

# newfor forms.py
# from django import forms

# class UploadFileForm(forms.Form):
#     file = forms.FileField()

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 10 MB',
        widget=forms.FileInput(attrs={'accept': 'text/csv', 'maxlength': '10MB'})
    )




