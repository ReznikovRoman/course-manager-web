from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import (User, AbstractUser, BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin, Permission, Group)

from django.utils import timezone
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

##################################################################################################################
from courses.models import CourseInstance, Course


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        if not username:
            raise ValueError("Users must have a username!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

    def get_or_create(self, email, username, password=None):
        created = True
        try:
            user = self.get(
                email=self.normalize_email(email),
                username=username,
            )
            created = False
        except CustomUser.DoesNotExist:
            user = self.create_user(
                email=self.normalize_email(email),
                username=username,
                password=password
            )
        return user, created


#############################################################################################################


def get_default_profile_pic():
    return 'images/profile_pics/default_profile_pics/user_1.png'


class CustomUser(AbstractUser, PermissionsMixin):
    # required fields
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # login parameter
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def get_all_permissions(self, obj=None):
        if self.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(group__user=self)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if perm in self.get_all_permissions() or perm in self.get_group_permissions():
            return True
        return False

    def has_module_perms(self, app_label):
        return True


class Address(models.Model):
    profile = models.OneToOneField("Profile", related_name='address', on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} | {self.zip_code}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)

    phone = PhoneNumberField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile_pics',
                                    default=get_default_profile_pic)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return f"Student - {self.pk}"


# ============== STAFF ============================= #################################################################

class StaffWorker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000),
        ]
    )

    @property
    def profile(self):
        return self.user.profile

    def save(self, *args, **kwargs):
        self.user.is_staff = True
        super(StaffWorker, self).save(*args, **kwargs)

    def __str__(self):
        return f"Staff | {self.profile.first_name} {self.profile.last_name} "


class Teacher(StaffWorker):
    supervised_courses = models.ManyToManyField(CourseInstance, related_name='teachers')

    def save(self, *args, **kwargs):
        teacher_group = Group.objects.get(name='teachers')
        teacher_group.user_set.add(self.user)
        super(Teacher, self).save(*args, **kwargs)


class Manager(StaffWorker):
    supervised_course_instances = models.ManyToManyField(CourseInstance, related_name='managers')
    supervised_courses = models.ManyToManyField(Course, related_name='managers')

    def save(self, *args, **kwargs):
        manager_group = Group.objects.get(name='managers')
        manager_group.user_set.add(self.user)
        super(Manager, self).save(*args, **kwargs)
