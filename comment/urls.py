from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # ex: /issue/create/
	path('create/', views.comment_create, name='comment_create'),
    # ex: /issue/2/delete/
    path('<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    # ex: /issue/2/detail/
    path('<int:comment_id>/detail/', views.comment_detail, name='comment_detail'),
    # ex: /issue/search/
    # path('search/', views.issue_search, name='comment_search'),
    # ex: /issue/2/answer_list/
    path('list/', views.comment_list, name='comment_list'),
    # ex: /issue/answer/3/like/
    path('<int:comment_id>/like/', views.comment_like, name='comment_like'),
]