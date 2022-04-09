from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('dashboard/', views.cms_dashboard, name='dashboard'),
    path('userip/', views.monitor_userip_view, name='userip'),
]
