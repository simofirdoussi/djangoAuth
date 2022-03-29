from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'type':'password',  'placeholder':'Password'}),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'type':'password',  'placeholder':'Confirm password'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

        widgets = {
            'email' : forms.TextInput(attrs = {'class': 'full-width', 'placeholder': 'Email' }),
            'username' : forms.TextInput(attrs = {'class': 'full-width', 'placeholder': 'Username' }),
        }

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class': 'full-width', 'placeholder': 'Email or Username' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'full-width', 'placeholder': 'Password' }))