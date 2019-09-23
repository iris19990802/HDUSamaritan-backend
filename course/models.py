from django.db import models
from users.models import User

class Course(models.Model):
    c_id = models.CharField(max_length=10)
    c_name = models.CharField(max_length=30)
    c_student = models.ManyToManyField(User,related_name="stu_course_st")
    c_teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tea_course_st")