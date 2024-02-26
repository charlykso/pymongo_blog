from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='register_user'),
    path('all', views.allUsers, name='all_users'),
    path('get/<int:id>', views.getUser, name='get_user'),
]