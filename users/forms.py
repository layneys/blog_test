from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    bio = forms.CharField(required=False)
    date_birth = forms.DateField(required=False)
    # password = forms.CharField(widget=forms.PasswordInput)
    # repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    bio = forms.CharField(required=False)
    date_birth = forms.DateField(required=False)
