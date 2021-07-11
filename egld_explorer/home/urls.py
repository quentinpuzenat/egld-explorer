from django.urls import path

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('principal_chart/', TemplateView.as_view(template_name="home/principal_chart.html"), name='principal_chart')
]