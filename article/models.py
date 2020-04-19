from django.db import models

# Create your models here.

class Article(models.Model):
    ''' 定义Article类
    '''
    ID = models.PositiveIntegerField(primary_key=True)    # ID of an article
    title = models.CharField(max_length=100)    # 标题
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)     # 作者
    pub_date = models.DateTimeField()    # 发布时间
    content = models.TextField()         # 文章内容，后续可能修改为MDText类型
    attention = models.ManyToManyField('account.User', on_delete=models.CASCADE)    # 关注/收藏者
    vote = models.ManyToManyField('account.User', on_delete=models.CASCADE)     # 点赞者
