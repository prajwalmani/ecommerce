from django import forms
from django.contrib.auth import get_user_model

user=get_user_model()

class GuestFrom(forms.Form):
    email=forms.EmailField()

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password ",widget=forms.PasswordInput)
    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=user.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User already exits")
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=user.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exits")
        return email
        
    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return data 
        
