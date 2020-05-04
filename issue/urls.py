from django.urls import path
from . import views

app_name = 'issue'

urlpatterns = [
    # ex: /issue/create/
	path('create/', views.issue_create, name='issue_create'),
    # ex: /issue/2/delete/
    path('<int:issue_id>/delete/', views.issue_delete, name='issue_delete'),
    # ex: /issue/2/detail/
    path('<int:issue_id>/detail/', views.issue_detail, name='issue_detail'),
    # ex: /issue/search/
    path('search/', views.issue_search, name='issue_search'),
    # ex: /issue/2/collect/
    path('<int:issue_id>/collect/', views.issue_collect, name='issue_collect'),
    # ex: /issue/collection_list/
    path('collection_list/', views.issue_collection_list, name='issue_collection_list'),
    # ex: /issue/2/like/
    path('<int:issue_id>/like/', views.issue_like, name='issue_like'),
    # ex: /issue/2/answer/create/
    path('<int:issue_id>/answer/create/', views.answer_create, name='answer_create'),
    # ex: /issue/answer/3/delete/
    path('answer/<int:answer_id>/delete/', views.answer_delete, name='answer_delete'),
    # ex: /issue/answer/3/detail/
    path('answer/<int:answer_id>/detail/', views.answer_detail, name='answer_detail'),
    # ex: /issue/2/answer_list/
    path('<int:issue_id>/answer_list/', views.answer_list, name='answer_list'),
    # ex: /issue/answer/3/like/
    path('answer/<int:answer_id>/like/', views.answer_like, name='answer_like'),
]