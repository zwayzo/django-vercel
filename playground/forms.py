from django import forms 
from .models import User

class SignUpForm(forms.ModelForm):  # Inherit from forms.ModelForm, not models.Model
    password = forms.CharField(widget=forms.PasswordInput)  # Add widget here for password

    class Meta:
        model = User
        fields = ['name', 'email', 'password']  # List the model fields to incl