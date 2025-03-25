from django.urls import path,include
from .views import *


urlpatterns = [
    path('Dashboard/', dashboard, name='dashboard'),
    path('dashboard/filter-stats/', filter_stats, name='filter_stats'),
    path('Dashboard/filter-stats/', filter_stats, name='filter_stats_alt'),
]
