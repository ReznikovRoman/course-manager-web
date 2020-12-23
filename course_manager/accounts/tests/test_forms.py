from django.test import TestCase, SimpleTestCase

import datetime

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


class UpdateProfileFormTest(SimpleTestCase):

    def test_bio_label(self):
        form = UpdateProfileForm()
        self.assertEquals(form.fields['bio'].label, 'Write something about yourself')

    def test_profile_pic_label(self):
        form = UpdateProfileForm()
        self.assertEquals(form.fields['profile_pic'].label, 'Upload your profile picture')

    def test_date_of_birth_correct(self):
        form = UpdateProfileForm(
            data={
                'date_of_birth': datetime.date(2002, 3, 7)
            }
        )
        self.assertTrue(form.is_valid())

    def test_date_of_birth_in_future(self):
        form = UpdateProfileForm(
            data={
                'date_of_birth': datetime.date(3000, 12, 12)
            }
        )
        self.assertFalse(form.is_valid())



