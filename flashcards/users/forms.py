from django import forms
from django.core.exceptions import ValidationError

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='E-Mail Address')
    password1 = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', max_length=100, widget=forms.PasswordInput)
    name = forms.CharField(label='Name (optional)', max_length=150, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        users = User.objects.filter(username=username)
        if users.count():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        users = User.objects.filter(email=email)
        if users.count():
            raise ValidationError('Email already in use')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1 and password2) and (password1 != password2):
            raise ValidationError('Passwords do not match')
        return password2

    def create_user(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password2'],
            last_name=self.cleaned_data['name']
        )
        return user
