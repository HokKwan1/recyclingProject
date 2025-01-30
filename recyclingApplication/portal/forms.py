from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    user_name = forms.CharField(label="Your Username", max_length=20, error_messages={
        "required": "Your username is required",
        "max_length": "Your username cannot exceeds 20 characters."
    })
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # To hide password input
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Ensure the new user is a volunteer
        if commit:
            user.set_password(self.cleaned_data["password"])  # Hash password before saving
            user.save()
        return user
    

class CustomPasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter current password"}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter new password"}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm new password"}),
    )
