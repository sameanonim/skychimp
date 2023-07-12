from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, AuthenticationForm, \
    PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from mailing_app.forms import StyleFormMixin
from users.models import User


class CustomUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'avatar')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class CustomUserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        field_classes = {'username': UsernameField}


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User


class CustomResetConfirmForm(SetPasswordForm):
    class Meta:
        model = User

