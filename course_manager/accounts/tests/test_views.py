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
    

























