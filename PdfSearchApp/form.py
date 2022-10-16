import email
from pyexpat import model
from django import forms
from .models import Files
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = "__all__"
        labels = {
            "title": "",
            "description": "",
            "file": "",
        }
        widgets = {
            "title": forms.HiddenInput(),
            "description": forms.HiddenInput(),
            "file": forms.FileInput(attrs={"accept": "application/pdf"}),
        }


# accept="image/png, image/gif, image/jpeg"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Invalid username or password')
