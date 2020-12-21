from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib import admin

from . import models

#######################################################################################################################


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', ),
        }),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user')
    readonly_fields = ('id', 'user')
    exclude = ('USERNAME_FIELD', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


######################################################################################################################


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)




