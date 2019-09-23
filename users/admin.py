from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'nickname','role', )
    search_fields = ('username', 'role')
    ordering = ('-id', )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Personal info', {'fields': ('nickname','image')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser' )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nickname', 'role', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)