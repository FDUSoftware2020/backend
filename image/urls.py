from django.urls import path
from . import views

app_name = 'image'

urlpatterns = [
    # ex: /image/upload/
	path('upload/', views.upload, name='upload'),
]