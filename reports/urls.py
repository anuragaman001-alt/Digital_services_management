from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sales_report, name='sales_report'),
    path('sales/export/', views.export_sales_csv, name='export_sales_csv'),
]
