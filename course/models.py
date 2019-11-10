from django.db import models
from users.models import User

class Course(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_code = models.CharField(max_length=10,default="C123456") #课程代码
    c_name = models.CharField(max_length=30)
    c_teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tea_course_st")

    cnt_sign = models.IntegerField(default=0) # 本课总签到次数
    #is_deleted = models.BooleanField(default=False) # is_deleted == False 表示已经删除


class Registration(models.Model): # 点名单（学生-班级多对多关系表）

    user= models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    cnt_abcense = models.IntegerField(default=0) # 指定学生在指定课程里的，实际 "到课" 次数

    is_quit = models.BooleanField(default=False) # is_quited == True 表示已经退课
