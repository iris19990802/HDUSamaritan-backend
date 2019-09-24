from django.db import models
from users.models import User
from course.models import Course


class Attendance(models.Model):
    A_id = models.AutoField(primary_key=True)
    A_course = models.ForeignKey(Course,on_delete=models.CASCADE)

    A_date = models.DateTimeField(auto_now=True)  # 签到发起时间（自动为True）


class student_attendance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    abcense = models.BooleanField()