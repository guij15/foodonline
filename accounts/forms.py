from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password']
    def clean(self):
        clean_data=super(UserForm,self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password Not Matched")

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')