from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Course,Registration


class CourseAdmin(admin.ModelAdmin):
    list_display = ('c_id','c_code', 'c_name', 'c_teacher','cnt_sign')
    search_fields = ('c_id','c_code','c_name', 'c_teacher','cnt_sign')
    ordering = ('-c_id', )

class Registration_Admin(admin.ModelAdmin):
    list_display = ('id','course','user', 'cnt_abcense' )
    search_fields = ('course','user', 'cnt_abcense')


admin.site.register(Course, CourseAdmin)
admin.site.register(Registration,Registration_Admin)