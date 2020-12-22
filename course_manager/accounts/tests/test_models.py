from django.test import TestCase, SimpleTestCase

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from accounts.models import (CustomUser, Address, Profile)

######################################################################################################################


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        CustomUser.objects.create_user(
            email='test1@gmail.com',
            username='test1',
            password='romanroman1',
        )

        CustomUser.objects.create_user(
            email='test2@gmail.com',
            username='test2',
            password='romanroman1',
        )

        # Create new ContentTypes
        test_content_type = ContentType.objects.get_for_model(CustomUser)

        # Create new permissions
        test_account_perm = Permission.objects.create(
            codename='can_test',
            name='Test Permission',
            content_type=test_content_type,
        )
        test_manager_perm = Permission.objects.create(
            codename='can_add_teacher',
            name='Test Manager Permission',
            content_type=test_content_type,
        )

        # Create new groups
        manager_group = Group.objects.create(name='managers')
        teacher_group = Group.objects.create(name='teachers')
        student_group = Group.objects.create(name='students')
        test_group = Group.objects.create(name='test')

        # Set permissions to the groups
        test_group.permissions.add(test_account_perm)
        manager_group.permissions.add(test_manager_perm)

        # Set groups to the users
        CustomUser.objects.get(pk=1).groups.add(test_group)
        CustomUser.objects.get(pk=2).groups.add(manager_group)
        CustomUser.objects.get(pk=2).groups.add(test_group)

    def test_email_max_length(self):
        user = CustomUser.objects.get(pk=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 60)

    def test_username_max_length(self):
        user = CustomUser.objects.get(pk=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEquals(max_length, 30)

    def test_email_label(self):
        user = CustomUser.objects.get(pk=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_date_joined_label(self):
        user = CustomUser.objects.get(pk=1)
        field_label = user._meta.get_field('date_joined').verbose_name
        self.assertEquals(field_label, 'date joined')

    def test_last_login_label(self):
        user = CustomUser.objects.get(pk=1)
        field_label = user._meta.get_field('last_login').verbose_name
        self.assertEquals(field_label, 'last login')

    def test_object_name_is_email(self):
        user = CustomUser.objects.get(pk=1)
        expected_object_name = str(user.email)
        self.assertEquals(str(user), expected_object_name)

    def test_has_perm_true(self):
        user = CustomUser.objects.get(pk=1)
        self.assertTrue(user.has_perm('accounts.can_test'))

    def test_has_perm_false(self):
        user = CustomUser.objects.get(pk=1)
        self.assertFalse(user.has_perm('accounts.can_add_teacher'))

    def test_has_perm_multiple_groups_true(self):
        user = CustomUser.objects.get(pk=2)
        self.assertTrue(user.has_perm('accounts.can_add_teacher'))

    def test_new_profile_on_create(self):
        user = CustomUser.objects.get(pk=1)
        self.assertIsNotNone(user.profile)

    def test_new_address_on_create(self):
        user = CustomUser.objects.get(pk=1)
        self.assertIsNotNone(user.profile.address)








