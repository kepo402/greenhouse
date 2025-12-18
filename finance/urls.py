from django.urls import path
from . import views

from .views import dashboard_api

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("api/dashboard/", dashboard_api, name="dashboard-api"),
]

