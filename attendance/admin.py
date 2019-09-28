from django.contrib import admin
from .models import Attendance,student_attendance
# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','A_course','A_date')
    search_fields = ('A_course','A_date')

class student_attendanceAdmin(admin.ModelAdmin):
    list_display = ('id','user','attendance','abcense')
    search_fields = ('user','attendance','abcense')

admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(student_attendance, student_attendanceAdmin)