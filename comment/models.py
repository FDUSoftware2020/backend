from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Comment(models.Model):
    """
    Define Comment Model, Level 1.
    """
    from_id = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="from_user")
    to_id = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="to_user")
    pub_date = models.DateTimeField()  # comment publish time
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # the type of the object it belongs to.
    object_id = models.PositiveIntegerField()  # answer id / article id / issue id
    content_object = GenericForeignKey('content_type', 'object_id')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True) #record the parent comment. if it's level 1 comment. it should be null.
    likers = models.ManyToManyField('account.User', related_name='comment_liker')

    def __str__(self):
        return str(self.id)