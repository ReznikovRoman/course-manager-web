from django.test import TestCase, SimpleTestCase

from accounts.forms import (CustomUserCreationForm, AddressForm, UpdateProfileForm)


###################################################################################################################


class CustomUserCreationFormTest(TestCase):

    def test_username_label(self):
        form = CustomUserCreationForm()
        self.assertEquals(form.fields['username'].label, 'Create a username')

    def test_email_label(self):
        form = CustomUserCreationForm()
        self.assertEquals(form.fields['email'].label, 'Email address')

    def test_different_passwords(self):
        form = CustomUserCreationForm(
            data={
                'username': 'form1',
                'email': 'form1@gmail.com',
                'password1': 'romanroman1',
                'password2': 'romanroman2',
            }
        )
        self.assertFalse(form.is_valid())

    def test_same_passwords(self):
        form = CustomUserCreationForm(
            data={
                'username': 'form1',
                'email': 'form1@gmail.com',
                'password1': 'romanroman1',
                'password2': 'romanroman1',
            }
        )
        self.assertTrue(form.is_valid())



