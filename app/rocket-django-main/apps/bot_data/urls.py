# bot_data/urls.py
from django.urls import path
from . import views

app_name = 'bot_data'

urlpatterns = [

    path('dashboard/', views.bot_dashboard, name='bot_dashboard'),
    path('leads/', views.bot_leads, name='bot_leads'),
    path('events/', views.bot_events, name='bot_events'),
    path('calculations/', views.bot_calculations, name='bot_calculations'),
    path('analytics/', views.bot_analytics, name='bot_analytics'),
    path('stats/', views.bot_stats_api, name='bot_stats_api'),
]

