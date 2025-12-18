from django.urls import path
from . import views

from .views import dashboard_api

urlpatterns = [
    path('', views.dashboard, name='dashboard'),         # /api/
    path('dashboard/', dashboard_api, name='dashboard-api'),  # /api/dashboard/
]
