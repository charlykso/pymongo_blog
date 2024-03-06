from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('create', views.create, name='register_user'),
    path('all', views.allUsers, name='all_users'),
    path('get/<int:pk>', views.getUser, name='get_user'),

    # auth
    path('signin/', views.MyTokenObtainPairView.as_view(), name='signin'),
]