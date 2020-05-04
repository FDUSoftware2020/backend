from django.contrib import admin
from .models import Issue, Answer

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ['replier', 'pub_date', 'content']
    extra = 0

class IssueAdmin(admin.ModelAdmin):
    # add list at the admin site
    list_display = ('Type', 'title', 'author', 'pub_date')
    # add search option at the admin site
    search_fields = ['Type', 'title', 'author']
    # classify the infomation of articles
    fieldsets = [
        ('Basic Information', {'fields': ['Type', 'title', 'author', 'pub_date']}),
        ('Content information', {'fields': ['content'], 'classes': ['collapse']}),
    ]
    # add choices at the bottom
    inlines = [AnswerInline]

# register Article
admin.site.register(Issue, IssueAdmin)