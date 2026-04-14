from django.urls import path
from . import views

urlpatterns = [
    # User
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('<int:pk>/deactivate/', views.deactivate_subscription, name='deactivate_subscription'),
    path('<int:pk>/reactivate/', views.reactivate_subscription, name='reactivate_subscription'),
    path('<int:pk>/change-plan/', views.upgrade_downgrade, name='upgrade_downgrade'),
    path('invoice/<int:pk>/download/', views.download_invoice, name='download_invoice'),
    # Admin
    path('admin/subscriptions/', views.admin_subscription_list, name='admin_subscription_list'),
    path('admin/subscriptions/<int:pk>/toggle/', views.admin_toggle_subscription, name='admin_toggle_subscription'),
]
