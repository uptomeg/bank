from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError({
                'username' : 'Username or password is invalid'}
            )
        data['user'] = user
        return data



class SignupForm(forms.ModelForm):
     password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(), error_messages={'min_length': 'This password is too short. It must contain at least 8 characters', 'required': 'This field is required'})
     password2 = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': 'This field is required'})
     class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name'
        ]
        error_messages = {
            'username': {'unique': 'A user with that username already exists', 'required': 'This field is required'},
            'email': {'invalid': 'Enter a valid email address'},
        }

     def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match")
        return password2

     """ def clean(self):
        errors = {}
        data = super().clean()
        if data['password'] != data['password2']:
            errors['password'] = "The two password fields didn't match"
        if User.objects.filter(username=data['username']).exists():
            errors['username'] = "A user with that username already exists"
        if len(data['password']) < 8:
            if 'password' not in errors.keys():
                errors['password'] = "This password is too short. It must contain at least 8 characters"
            else:
                errors['password'] = errors['password'] + "This password is too short. It must contain at least 8 characters"
        if not validate_email(data['email']):
            errors['email'] = "Enter a valid email address"
        if data['username'] is None or data['username'] == '':
            if 'username' not in errors.keys():
                errors['username'] = "This field is required"
            else:
                errors['username'] = errors['username'] + "This field is required"
        if data['password'] is None or data['password'] == '':
            if 'password' not in errors.keys():
                errors['password'] = "This field is required"
            else:
                errors['password'] = errors['password'] + "This field is required"
        if data['password2'] is None or data['password2'] == '':
            errors['password2'] = "This field is required"
        if errors != {}:
            raise ValidationError(errors)
        return data """


     """ class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
 """


""" Endpoint: /accounts/register/ 
Methods: GET, POST
Fields/payload: username, password1, password2, email, first_name, last_name
Success URL: /accounts/login/ 
Validation errors: (copy and paste the exact error message)
The two password fields didn't match
A user with that username already exists
This password is too short. It must contain at least 8 characters
Enter a valid email address
Username, password, and repeat password are required. If empty, show the following error above the problematic field: 
This field is required
Additional notes: In our tests, no field will be more than 120 characters long.
"""

class EditProfileForm(forms.ModelForm):
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=False, error_messages={'min_length': 'This password is too short. It must contain at least 8 characters'})
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        error_messages = {
            'email': {'invalid': 'Enter a valid email address'},
        }
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise ValidationError("The two password fields didn't match")
        return password2
