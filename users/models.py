from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    u_role = models.IntegerField(default=2)
    u_nickname = models.CharField(max_length=20)

    def get_file_path(self,filename):
         ext = filename.split('.')[-1]
         if ext == "jpeg":
             ext = "jpg"
         return 'static/identities/%s_0.%s' % (self.username,ext)

    def get_file_path_1(self,filename):
         ext = filename.split('.')[-1]
         if ext == "jpeg":
             ext = "jpg"
         return 'static/identities/%s_1.%s' % (self.username,ext)

    def get_file_path_2(self,filename):
         ext = filename.split('.')[-1]
         if ext == "jpeg":
             ext = "jpg"
         return 'static/identities/%s_2.%s' % (self.username,ext)

    u_image_0 = models.ImageField(upload_to=get_file_path,null=True) # 正面照
    u_image_1 = models.ImageField(upload_to=get_file_path_1,null=True) # 左侧面照
    u_image_2 = models.ImageField(upload_to=get_file_path_2,null=True) # 右侧面照

    def return_role(self):
        role_name = ""
        if self.role == 1:
            role_name = "教师"
        elif self.role == 2:
            role_name = "学生"
        elif self.role == 0:
            role_name = "管理员"
        return role_name
