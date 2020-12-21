from django.shortcuts import render
from django.views import generic

from . import models as account_models
from . import forms as account_forms

##############################################################################################################


class ProfileCreate(generic.UpdateView):
    model = account_models.Profile
    form_class = account_forms.UpdateProfileForm
    template_name = 'accounts/test_profile_form.html'

    def get(self, request, *args, **kwargs):
        profile_form = account_forms.UpdateProfileForm(prefix='profile')
        address_form = account_forms.AddressForm(prefix='address')
        return render(request, 'accounts/test_profile_form.html', {
            'profile_form': profile_form,
            'address_form': address_form,
        })

    def post(self, request, *args, **kwargs):
        profile_form = account_forms.UpdateProfileForm(request.POST, prefix='profile')
        address_form = account_forms.AddressForm(request.POST, prefix='address')

        if profile_form.is_valid() and address_form.is_valid():
            address_form.save()
            profile_form.cleaned_data['address'] = address_form
            profile_form.save()

            print("Done!")
        return render(request, 'accounts/test_profile_form.html', {
            'profile_form': profile_form,
            'address_form': address_form,
        })








