from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

from . import models as account_models

##################################################################################################################


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = account_models.CustomUser

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Create a username'
        self.fields['email'].label = 'Email address'


class AddressForm(forms.ModelForm):
    class Meta:
        model = account_models.Address
        exclude = ('profile', )
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - date of birth in the future'))
        return data

    class Meta:
        model = account_models.Profile
        exclude = ('address', 'user', )
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'input_field'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].label = 'Write something about yourself'
        self.fields['profile_pic'].label = 'Upload your profile picture'








