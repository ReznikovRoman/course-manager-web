from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

from . import models as account_models

##################################################################################################################


class AddressForm(forms.ModelForm):
    class Meta:
        model = account_models.Address
        fields = '__all__'


class UpdateProfileForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - date of birth in the future'))
        return data

    class Meta:
        model = account_models.Profile
        exclude = ('address', )








