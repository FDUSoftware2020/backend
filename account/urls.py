from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # ex: /account/login
	path('login/', views.login, name='login'),
    # ex: /account/register
	path('register/', views.register, name='register'),
    # ex: /account/logout
    path('logout/', views.logout, name='logout'),
]