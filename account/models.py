from django.db import models

# Create your models here.

class User(models.Model):
    ''' 用户类
    '''

    username = models.CharField(max_length=100, unique=True)  # 用户名
    email = models.CharField(max_length=100, unique=True)  # 学邮
    password = models.CharField(max_length=100, default="")  # 密码
    cookie_value = models.CharField(max_length=200, default="")  # cookie值
    signature = models.TextField(default="他(她)什么也没留下~")  # 个性签名
    contribution = models.PositiveIntegerField(default=0)  # 贡献值

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    ''' 验证码类
    '''

    email = models.CharField(max_length=100, unique=True)  # 邮箱
    code = models.CharField(max_length=4, default="")  # 验证码
    make_time = models.DateTimeField()  # 验证码生成时刻

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    ''' 消息通知类
    '''

    class MsgType(models.IntegerChoices):
        AnswerToIssue = 0
        CommentToArticle = 1
        CommentToAnswer = 2

    Type = models.IntegerField(choices=MsgType.choices)
    issue_id = models.IntegerField()
    answer_id = models.IntegerField()
    parent_comment_id = models.IntegerField()
    comment_id = models.IntegerField()
    from_uname = models.CharField(max_length=100, default="无名氏")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rec_msg')
    pub_date = models.DateTimeField()
    content = models.TextField()
    IsReading = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)