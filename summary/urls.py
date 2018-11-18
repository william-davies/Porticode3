from django.urls import path
from django.views.generic import TemplateView

from summary.views import SummaryView

app_name = 'summary'

urlpatterns = [
    path('', SummaryView.as_view(), name='summary'),
]