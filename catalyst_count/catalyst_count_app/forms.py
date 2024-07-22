from allauth.account.forms import LoginForm
from .models import File
from django import forms

class CustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        # Add custom authentication logic here if needed
        return super(CustomLoginForm, self).login(*args, **kwargs)
    

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']