from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    u_role = models.IntegerField(default=2)
    u_nickname = models.CharField(max_length=20)
    def get_file_path(self,filename):
        ext = filename.split('.')[-1]
        return 'static/identities/%s.%s' % (self.username,ext)

    u_image = models.ImageField(upload_to=get_file_path,null=True)

    def return_role(self):
        role_name = ""
        if self.role == 1:
            role_name = "教师"
        elif self.role == 2:
            role_name = "学生"
        elif self.role == 0:
            role_name = "管理员"
        return role_name
