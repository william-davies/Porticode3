from django.urls import path
from django.views.generic import TemplateView

from dashboard.views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]