from django.contrib import admin

# Register your models here.
from comment.models import Comment


# class CommentInline(admin.TabularInline):
#     model = Comment
#     fields = ["from_id", "to_id", "pub_date", "content", "parent_comment"]
#     extra = 0

admin.site.register(Comment)