from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # ex: /comment/create/
	path('create/', views.comment_create, name='comment_create'),
    # ex: /comment/2/delete/
    path('<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    # ex: /comment/2/detail/
    path('<int:comment_id>/detail/', views.comment_detail, name='comment_detail'),
    # ex: /comment/list/
    path('list/', views.comment_list, name='comment_list'),
    # ex: /comment/3/like/
    path('<int:comment_id>/like/', views.comment_like, name='comment_like'),
]