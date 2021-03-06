from django.db import models

# Create your models here.

class Issue(models.Model):
    ''' 定义Issue类
    '''

    class IssueType(models.IntegerChoices):
        ISSUE = 0
        ARTICLE = 1

    Type = models.IntegerField(choices=IssueType.choices)                                                # 类型, issue or article
    title = models.CharField(max_length=100)                                                             # 标题
    author = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='create_issue')    # 作者
    pub_date = models.DateTimeField()                                                                    # 发布时间
    content = models.TextField()                                                                         # 详细内容
    collectors = models.ManyToManyField('account.User', related_name='collect_issue')                    # 收藏者
    likers = models.ManyToManyField('account.User', related_name='like_issue')                           # 点赞者

    def __str__(self):
        return str(self.id)


class Answer(models.Model):
    ''' 定义Answer类，即对Issue的回答
    '''
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)                         # 回答的Isssue
    replier = models.ForeignKey('account.User', on_delete=models.CASCADE)              # 回答者
    pub_date = models.DateTimeField()                                                  # 回答时间
    content = models.TextField()                                                       # 回答的内容
    likers = models.ManyToManyField('account.User', related_name='like_answer')        # 点赞者

    def __str__(self):
        return str(self.id)
    