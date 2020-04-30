from django.contrib import admin
from .models import User, VerificationCode

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'contribution')
    fields = ['username', 'email', 'password', 'signature', 'contribution']
    search_fields = ['username', 'email']


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'make_time')
    fields = ['email', 'code', 'make_time']
    search_fields = ['email']


admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)