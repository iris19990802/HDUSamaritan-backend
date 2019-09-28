from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'u_nickname','u_role', 'u_image_0','u_image_1','u_image_2')
    #list_display = ( 'username', 'u_nickname','u_role', 'u_image')
    search_fields = ('username', 'u_role')
    ordering = ('-id', )
    fieldsets = (
        #(None, {'fields': ('id','username', 'password', 'u_role')}),
        (None, {'fields': ('username', 'password', 'u_role')}),
        ('Personal info', {'fields': ('u_nickname','u_image_0','u_image_1','u_image_2')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser' )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'u_nickname', 'u_role', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)