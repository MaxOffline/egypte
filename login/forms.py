from django import forms
from django.contrib.auth.models import User
from login.models import userProfile


class Register(forms.ModelForm):
    username        = forms.CharField(
                    max_length = 12,
                    widget     =  forms.TextInput(
                                attrs={'placeholder': "Username"}
                            ))
    password        = forms.CharField(
                    max_length = 25,
                    widget     = forms.PasswordInput(
                                attrs={'placeholder': "Password"}
                            ))
    ConfirmPassword = forms.CharField(
                    max_length = 25,

                    label  = "Confirm Password",
                    widget = forms.PasswordInput(
                            attrs={'placeholder': "Confirm Password"}
                            ))
    email           = forms.CharField(
                    max_length = 50,
                    widget     =  forms.TextInput(
                                attrs={'placeholder': "Email"}
                            ))
    ConfirmEmail    = forms.CharField(
                    max_length = 50,
                    label  = "Confirm Email",
                    widget =  forms.TextInput(
                            attrs={'placeholder': "Confirm Email"}
                            ))

    class Meta:

        model = User
        fields = (
                "username",
                "password",
                "ConfirmPassword",
                "email",
                "ConfirmEmail",
                )



