from django.db import models

# Create your models here.

class Issue(models.Model):
    ''' 定义Issue类
    '''
    asker = models.ForeignKey('account.User', on_delete=models.CASCADE)  # 提问者
    pub_date = models.DateTimeField()    # 提问时间
    content = models.TextField()    # issue的内容，后续可能修改为MDText类型
    attention = models.ManyToManyField('account.User', on_delete=models.CASCADE)    # 关注/收藏者


class Answer(models.Model):
    ''' 定义Answer类，即对Issue的回答
    '''
    ID = models.PositiveIntegerField(primary_key=True)     # ID of an answer
    issue = models.ForeignKey(Issue, on_delete=models.CSCADE)     # 回答的Isssue
    replier = models.ForeignKey('account.User', on_delete=models.CASCADE)     # 回答者
    pub_date = models.DateTimeField()    # 提问时间
    content = models.TextField()    # 回答的内容，后续可能修改为MDText类型
    vote = models.ManyToManyField('account.User', on_delete=models.CASCADE)     # 点赞者

