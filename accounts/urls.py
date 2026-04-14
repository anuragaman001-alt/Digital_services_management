from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Password reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    # Profile
    path('profile/', views.user_profile, name='user_profile'),
    # Admin - Users
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:pk>/update/', views.admin_user_update, name='admin_user_update'),
    path('admin/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
]
