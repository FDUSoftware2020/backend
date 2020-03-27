from django.contrib import admin
from .models import User, VerificationCode

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'password', 'cookie_value']
    list_display = ('username', 'email', 'password')
    search_fields = ['username', 'email']


class VerificationCodeAdmin(admin.ModelAdmin):
    fields = ['email', 'code', 'make_time']
    list_display = ('email', 'code', 'make_time')
    search_fields = ['email']


admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)