from django import forms
from django.contrib.auth.models import User



class Register(forms.ModelForm):
    username        = forms.CharField(max_length = 12)
    password        = forms.CharField(max_length = 15, widget = forms.PasswordInput)
    ConfirmPassword = forms.CharField(max_length = 15, widget = forms.PasswordInput, label = "Confirm Password")
    ConfirmEmail    = forms.CharField(label = "Confirm Email")

    class Meta:

        model = User
        fields = ("username" , "password" , 'ConfirmPassword', "email" ,  'ConfirmEmail')
