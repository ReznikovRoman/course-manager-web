from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Permission

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


######################################################################################################################


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)

admin.site.register(Permission)




