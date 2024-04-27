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

