from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('create', views.create, name='register_user'),
    path('all', views.allUsers, name='all_users'),
    path('get/<int:pk>', views.getUser, name='get_user'),
    path('update/<int:pk>', views.updateUser, name='update_user'),
    path('delete/<int:pk>', views.deleteUser, name='delete_user'),
    path('profiles', views.get_profiles, name='get_profiles'),
    path('profile/<int:pk>', views.get_profile, name='get_profile'),
    path('<int:pk>/profile', views.get_user_profile, name='get_user_profile'),
    path('update_profile/<int:pk>', views.update_profile, name='update_profile'),

    # auth
    path('signin/', views.MyTokenObtainPairView.as_view(), name='signin'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]