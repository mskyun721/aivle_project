from . import views
from django.urls import path


app_name = 'api'
urlpatterns = [
    path('chart_all', views.chartAll, name='chart_all'),
]
