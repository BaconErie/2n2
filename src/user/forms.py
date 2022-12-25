from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import check_password

from .models import User

def validate_unique_username(username):
    '''Makes sure that the username doesn't already exist'''

    if User.objects.filter(username=username).count() != 0:
        raise ValidationError('Username already exists.')
  

class SignupForm(forms.Form):
    username = forms.CharField(label='Username (max length 20)', max_length=20, validators=[validate_unique_username])
    password = forms.CharField(label='Password (min length 8)', widget=forms.PasswordInput, validators=[MinLengthValidator(8, 'Password must be at least 8 characters long.')])
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('subject')
        confirm_password = cleaned_data.get('password')

        # Make sure password and confirm_password match
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationError('Username or password is incorrect. Please try again.')
        
        if password and not check_password(password, user.hashed_password):
            raise ValidationError('Username or password is incorrect. Please try again.')