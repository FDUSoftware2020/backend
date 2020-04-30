from django.urls import path
from . import views

app_name = 'issue'

urlpatterns = [
    # ex: /account/register/
	path('create/', views.create, name='create'),
    path('<int:issue_id>/delete/', views.delete, name='delete'),
    path('<int:issue_id>/detail/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('<int:issue_id>/collect/', views.collect, name='collect'),
    path('collection_list/', views.collection_list, name='collection_list'),
    path('<int:issue_id>/like/', views.issue_like, name='issue_like'),
    
]