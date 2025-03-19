from django import forms
from .models import Request
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class CreateRequestForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed."
    )

    phone = forms.CharField(
        max_length=20, 
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    postal_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Enter postal code'})
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should only contain letters.")
        return last_name

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isalnum():
            raise ValidationError("Postal code should only contain letters and numbers.")
        return postal_code

    class Meta:
        model = Request
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'city', 'state', 'country', 'postal_code']


class RequestByTokenForm(forms.Form):
    token = forms.CharField(max_length=512, required=True, label="Enter token")