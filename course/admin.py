from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'c_name', 'c_teacher')
    search_fields = ('c_id','c_name', 'c_teacher')
    ordering = ('-c_id', )

admin.site.register(Course, CourseAdmin)