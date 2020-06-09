from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # ex: /account/register
	path('register/', views.register, name='register'),
    # ex: /account/login
	path('login/', views.login, name='login'),
    # ex: /account/logout
    path('logout/', views.logout, name='logout'),
    # ex: /account/verify
	path('verify/', views.verify, name='verify'),
    # ex: /account/modify_password
	path('modify_password/', views.modify_password, name='modify_password'),
    # ex: /account/modify_username
	path('modify_username/', views.modify_username, name='modify_username'),
    # ex: /account/modify_signature
	path('modify_signature/', views.modify_signature, name='modify_signature'),
    # ex: /account/ask_login_user
	path('ask_login_user/', views.ask_login_user, name='ask_login_user'),
    # ex: /account/ask_user
	path('ask_user/', views.ask_user, name='ask_user'),
    # ex: /account/message/list
    path('message/list/', views.message_list, name='msg_list'),
    # ex: /account/message/3/read
    path('message/<int:msg_id>/read/', views.message_read, name='msg_read'),
    # ex: /account/message/4/delete
    path('message/<int:msg_id>/delete/', views.message_delete, name='msg_del'),
]