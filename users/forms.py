from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mailing.forms import StyleFormMixin
from users.models import User


class UserCreateForm(UserCreationForm, StyleFormMixin):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',  'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
        self.fields['email'].disabled = True


class UserManagerForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active',)
