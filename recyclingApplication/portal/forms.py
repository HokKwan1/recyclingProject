from django import forms
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
    user_name = forms.CharField(label="Your Username", max_length=20, error_messages={
        "required": "Your username is required",
        "max_length": "Your username cannot exceeds 20 characters."
    })
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
