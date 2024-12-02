from django import forms 
from .models import User, Team, myProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User



class SignUpForm(forms.ModelForm):  # Inherit from forms.ModelForm, not models.Model
    password = forms.CharField(widget=forms.PasswordInput)  # Add widget here for password

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # List the model fields to incl
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = myProfile
        fields = ['first_name', 'last_name', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'email', 'phoneNumber']