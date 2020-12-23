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


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new User
        user = CustomUser.objects.create_user(
            email='profile1@gmail.com',
            username='profile1',
            password='romanroman1',
        )

    def test_first_name_max_length(self):
        profile = CustomUser.objects.get(pk=1).profile
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 40)

    def test_last_name_max_length(self):
        profile = CustomUser.objects.get(pk=1).profile
        max_length = profile._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 40)

    def test_phone_max_length(self):
        profile = CustomUser.objects.get(pk=1).profile
        max_length = profile._meta.get_field('phone').max_length
        self.assertEquals(max_length, 20)

    def test_profile_pic_upload_folder(self):
        profile = CustomUser.objects.get(pk=1).profile
        profile_pic_upload_folder = profile._meta.get_field('profile_pic').upload_to
        self.assertEquals(
            profile_pic_upload_folder,
            'images/profile_pics'
        )

    def test_profile_pic_url_default(self):
        profile = CustomUser.objects.get(pk=1).profile
        profile_pic_url = profile.profile_pic
        self.assertEquals(
            profile_pic_url,
            'images/profile_pics/default_profile_pics/user_1.png'
        )

    def test_object_name_is_first_name_space_last_name(self):
        profile = CustomUser.objects.get(pk=1).profile
        setattr(profile, 'first_name', 'Roman')
        setattr(profile, 'last_name', 'Reznikov')
        profile.save()

        profile_object_name = str(profile)
        self.assertEquals(profile_object_name, 'Roman Reznikov')


class AddressModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user = CustomUser.objects.create_user(
            email='address1@gmail.com',
            username='address1',
            password='romanroman1',
        )

        # Update profile
        profile = user.profile
        setattr(profile, 'first_name', 'Roman')
        setattr(profile, 'last_name', 'Reznikov')
        setattr(profile, 'phone', '+79851686043')
        profile.save()

        # Update Address
        address = profile.address
        attrs = {
            'country': 'Russia',
            'city': 'Moscow',
            'street': 'Arbat',
            'zip_code': '1812813',
        }
        for name, value in attrs.items():
            setattr(address, name, value)
        address.save()

    def test_country_max_length(self):
        address = CustomUser.objects.get(pk=1).profile.address
        max_length = address._meta.get_field('country').max_length
        self.assertEquals(max_length, 100)

    def test_city_max_length(self):
        address = CustomUser.objects.get(pk=1).profile.address
        max_length = address._meta.get_field('city').max_length
        self.assertEquals(max_length, 100)

    def test_street_max_length(self):
        address = CustomUser.objects.get(pk=1).profile.address
        max_length = address._meta.get_field('street').max_length
        self.assertEquals(max_length, 100)

    def test_zip_code_max_length(self):
        address = CustomUser.objects.get(pk=1).profile.address
        max_length = address._meta.get_field('zip_code').max_length
        self.assertEquals(max_length, 20)

    def test_verbose_name_singular_is_address(self):
        address = CustomUser.objects.get(pk=1).profile.address
        verbose_name = address._meta.verbose_name
        self.assertEquals(verbose_name, 'address')

    def test_verbose_name_plural_is_addresses(self):
        address = CustomUser.objects.get(pk=1).profile.address
        verbose_name = address._meta.verbose_name_plural
        self.assertEquals(verbose_name, 'addresses')

    def test_object_name(self):
        address = CustomUser.objects.get(pk=1).profile.address
        object_name = str(address)
        self.assertEquals(
            object_name,
            'Russia, Moscow, Arbat | 1812813'
        )








