from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=100)  # 用户名
    password = models.CharField(max_length=100)  # 密码
    email = models.CharField(max_length=100, default="@fudan.edu.cn")  # 学邮
    cookie_value = models.CharField(max_length=200 , default="")  # cookie值

    def _str_(self):
        return self.username