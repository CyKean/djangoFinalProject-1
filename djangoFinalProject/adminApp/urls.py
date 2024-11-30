from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('predictions/', views.prediction_table, name='prediction_table'),
    path('export-measurements/', views.export_measurements, name='export_measurements'),
]