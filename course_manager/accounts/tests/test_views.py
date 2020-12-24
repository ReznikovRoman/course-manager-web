from django.test import TestCase, SimpleTestCase

from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ugettext_lazy as _

import datetime

from accounts.models import (CustomUser, Address, Profile)
from accounts.forms import CustomUserCreationForm, AddressForm, UpdateProfileForm


#######################################################################################################################


class SignUpViewTest(TestCase):

    def setUp(self) -> None:
        user1 = CustomUser.objects.create_user(
            email='view1@gmail.com',
            username='view1',
            password='romanroman1'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_view_correct_redirect(self):
        response = self.client.post(
            reverse('accounts:signup'),
            data={
                'username': 'view2',
                'email': 'view2@gmail.com',
                'password1': 'romanroman1',
                'password2': 'romanroman1',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], reverse('accounts:login'))

    def test_redirects_if_logged_in(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:signup'))
        self.assertRedirects(response, '/')


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        user1 = CustomUser.objects.create_user(
            email='view1@gmail.com',
            username='view1',
            password='romanroman1'
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_view_correct_redirect(self):
        response = self.client.post(
            reverse('accounts:login'),
            data={
                'username': 'view1@gmail.com',
                'password': 'romanroman1',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/')

    def test_redirect_if_logged_in(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, '/')


class EditProfileViewTest(TestCase):

    def setUp(self) -> None:
        user1 = CustomUser.objects.create_user(
            email='view1@gmail.com',
            username='view1',
            password='romanroman1'
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:profile'))
        self.assertTemplateUsed(response, 'accounts/profile_form.html')

    def test_restrict_view_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertURLEqual(
            response.url,
            f"{reverse('accounts:login')[1:]}?next={reverse('accounts:profile')}"
        )

    def test_form_invalid_death_of_birth(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.post(
            reverse('accounts:profile'),
            data={
                'date_of_birth': datetime.date(3000, 12, 12)
            }
        )
        error_invalid = [_('Invalid date - date of birth in the future')]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'date_of_birth', error_invalid)

    def test_redirects_to_profile_page_on_success(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.post(
            reverse('accounts:profile'),
            data={
                'first_name': 'Roman',
                'last_name': 'Reznikov',
                'bio': "I'm 18 years old",
                'date_of_birth': datetime.date(2002, 3, 7),
                'phone': '+79851686043'
            }
        )
        self.assertRedirects(response, reverse('accounts:profile'))

    def test_view_displays_only_current_user_details(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        # Update profile details
        profile = CustomUser.objects.get(pk=1).profile
        attrs = {
            'first_name': 'Roman',
            'last_name': 'Reznikov',
            'bio': "I'm 18 years old",
            'date_of_birth': datetime.date(2002, 3, 7),
            'phone': '+79851686043'
        }
        for name, value in attrs.items():
            setattr(profile, name, value)
        profile.save()

        response = self.client.get(reverse('accounts:profile'))
        for name, value in attrs.items():
            self.assertEqual(
                response.context['form'].initial[name],
                value
            )


class EditAddressViewTest(TestCase):

    def setUp(self) -> None:
        user1 = CustomUser.objects.create_user(
            email='view1@gmail.com',
            username='view1',
            password='romanroman1'
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get('/accounts/profile/address/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:profile-address'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        response = self.client.get(reverse('accounts:profile-address'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/address_form.html')

    def test_restrict_view_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:profile-address'))
        self.assertURLEqual(
            response.url,
            f"{reverse('accounts:login')[1:]}?next={reverse('accounts:profile-address')}"
        )

    def test_view_displays_only_current_user_details(self):
        self.client.login(email='view1@gmail.com', password='romanroman1')
        # Update address details
        address = CustomUser.objects.get(pk=1).profile.address
        attrs = {
            'country': 'Russia',
            'city': 'Moscow',
            'street': "Arbat",
            'zip_code': '137317',
        }
        for name, value in attrs.items():
            setattr(address, name, value)
        address.save()

        response = self.client.get(reverse('accounts:profile-address'))
        for name, value in attrs.items():
            self.assertEqual(
                response.context['form'].initial[name],
                value
            )


















