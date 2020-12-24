from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models

#######################################################################################################################


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_manager', 'is_teacher', 'is_student')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', ),
        }),
    )

    filter_horizontal = ()
    list_filter = ('groups__name', )
    fieldsets = ()

    def is_manager(self, obj):
        return obj.groups.filter(name='managers').exists()

    def is_teacher(self, obj):
        return obj.groups.filter(name='teachers').exists()

    def is_student(self, obj):
        return obj.groups.filter(name='students').exists()

    is_manager.boolean = True
    is_teacher.boolean = True
    is_student.boolean = True


class AddressAdmin(admin.ModelAdmin):
    list_display = ('profile', 'country', 'city', 'street')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    readonly_fields = ('id',)
    exclude = ('USERNAME_FIELD', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_supervised_courses')
    exclude = ('USERNAME_FIELD', )

    filter_horizontal = ('supervised_courses', )
    list_filter = ()
    fieldsets = ()
    ordering = ()
    readonly_fields = ('get_user_link', )

    def get_supervised_courses(self, obj):
        if obj.supervised_courses.all():
            return "; ".join([str(course) for course in obj.supervised_courses.all()])
        else:
            return '-'

    def get_user_link(self, obj: models.Teacher):
        return mark_safe(
            f"""<a href="{reverse('admin:accounts_teacher_change', args=(obj.user.pk,))}">{obj.user}</a>"""
        )

    get_user_link.short_description = 'user link'


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_supervised_courses', 'get_supervised_course_instances')
    exclude = ('USERNAME_FIELD', )

    filter_horizontal = ('supervised_courses', 'supervised_course_instances', )
    list_filter = ()
    fieldsets = ()
    ordering = ()
    readonly_fields = ('get_user_link', )

    def get_user_link(self, obj: models.Manager):
        return mark_safe(
            f"""<a href="{reverse('admin:accounts_customuser_change', args=(obj.user.pk,))}">{obj.user}</a>"""
        )

    def get_supervised_courses(self, obj):
        if obj.supervised_courses.all():
            return "; ".join([str(course) for course in obj.supervised_courses.all()])
        else:
            return '-'

    def get_supervised_course_instances(self, obj):
        if obj.supervised_courses.all():
            return "; ".join([str(course_i) for course_i in obj.supervised_course_instances.all()])
        else:
            return '-'

    get_user_link.short_description = 'user link'


######################################################################################################################


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)

admin.site.register(Permission)

admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Manager, ManagerAdmin)


