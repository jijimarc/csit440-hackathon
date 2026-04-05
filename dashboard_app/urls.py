from django.urls import path
from . import views

app_name = "dashboard_app"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('help/', views.help, name='help'),
    path('api/notifications/', views.student_notifications_api, name='student_notifications_api'),
    path('api/notifications/clear/', views.clear_student_notifications_api, name='clear_student_notifications_api'),
]