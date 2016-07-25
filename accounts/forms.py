import django.contrib.auth.forms as auth_forms
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(auth_forms.UserCreationForm):

    first_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
