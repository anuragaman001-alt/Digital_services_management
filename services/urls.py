from django.urls import path
from . import views

urlpatterns = [
    # User
    path('', views.plan_list, name='plan_list'),
    path('<int:pk>/', views.plan_detail, name='plan_detail'),
    # Admin
    path('admin/plans/', views.admin_plan_list, name='admin_plan_list'),
    path('admin/plans/create/', views.admin_plan_create, name='admin_plan_create'),
    path('admin/plans/<int:pk>/update/', views.admin_plan_update, name='admin_plan_update'),
    path('admin/plans/<int:pk>/delete/', views.admin_plan_delete, name='admin_plan_delete'),
    path('admin/plans/<int:pk>/toggle/', views.admin_plan_toggle, name='admin_plan_toggle'),
]
