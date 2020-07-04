from django import forms
from django.contrib.auth.forms import UserCreationForm

from flashcards.users.models import User


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(label='E-Mail Address')
    last_name = forms.CharField(label='Name (optional)', max_length=150, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'last_name'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
