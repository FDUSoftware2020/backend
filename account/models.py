from django.db import models

# Create your models here.

class User(models.Model):
    ''' 用户类
    '''

    username = models.CharField(max_length=100)  # 用户名
    password = models.CharField(max_length=100)  # 密码
    email = models.CharField(max_length=100, default="@fudan.edu.cn")  # 学邮
    cookie_value = models.CharField(max_length=200 , default="")  # cookie值
    
    def _str_(self):
        return self.username


class VerificationCode(models.Model):
    ''' 用户的验证码类
    '''

    email = models.CharField(max_length=100)  # 邮箱
    code = models.CharField(max_length=4)       # 验证码
    time = models.DateTimeField()  # 生成验证码时刻