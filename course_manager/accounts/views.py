from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

from . import models as account_models
from . import forms as account_forms

##############################################################################################################


class SignUp(generic.CreateView):
    form_class = account_forms.CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(SignUp, self).get(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).get(request, *args, **kwargs)


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = account_models.Profile
    form_class = account_forms.UpdateProfileForm
    template_name = 'accounts/profile_form.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        return {
            'bio': self.request.user.profile.bio,
            'first_name': self.request.user.profile.first_name,
            'last_name': self.request.user.profile.last_name,
            'date_of_birth': self.request.user.profile.date_of_birth,
            'profile_pic': self.request.user.profile.profile_pic,
            'phone': self.request.user.profile.phone,
        }
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user.profile = self.request.user.profile
        self.object.save()
        return super(EditProfileView, self).form_valid(form)


class EditAddressView(LoginRequiredMixin, generic.UpdateView):
    model = account_models.Address
    form_class = account_forms.AddressForm
    template_name = 'accounts/address_form.html'
    context_object_name = 'address'
    success_url = reverse_lazy('accounts:profile-address')

    def get_object(self, queryset=None):
        return self.request.user.profile.address

    def get_initial(self):
        return {
            'country': self.request.user.profile.address.country,
            'city': self.request.user.profile.address.city,
            'street': self.request.user.profile.address.street,
            'zip_code': self.request.user.profile.address.zip_code,
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object.save()
        return super(EditAddressView, self).form_valid(form)







