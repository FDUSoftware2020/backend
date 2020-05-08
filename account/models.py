from django.db import models

# Create your models here.

class User(models.Model):
    ''' 用户类
    '''

    username = models.CharField(max_length=100, unique=True)      # 用户名
    email = models.CharField(max_length=100, unique=True)         # 学邮
    password = models.CharField(max_length=100, default="")       # 密码
    cookie_value = models.CharField(max_length=200 , default="")  # cookie值
    signature = models.TextField(default="他(她)什么也没留下~")     # 个性签名
    contribution = models.PositiveIntegerField(default=0)         # 贡献值
    
    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    ''' 验证码类
    '''

    email = models.CharField(max_length=100, unique=True)  # 邮箱
    code = models.CharField(max_length=4, default="")      # 验证码
    make_time = models.DateTimeField()                     # 验证码生成时刻

    def __str__(self):
        return str(self.id)