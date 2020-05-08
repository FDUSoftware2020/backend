from django.contrib import admin
from .models import User, VerificationCode

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'contribution')
    fields = ['username', 'email', 'password', 'signature']
    search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)
