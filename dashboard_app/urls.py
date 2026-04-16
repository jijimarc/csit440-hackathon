from django.urls import path
from . import views

app_name = "dashboard_app"

urlpatterns = [
    # The main router (e.g., http://127.0.0.1:8000/dashboard/)
    path('', views.dashboard_router, name='dashboard'),
    
    # Specific Dashboards
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    
    # Account Pages
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('help/', views.help, name='help'),
    
    # JavaScript APIs
    path('api/notifications/', views.student_notifications_api, name='student_notifications_api'),
    path('api/notifications/clear/', views.clear_student_notifications_api, name='clear_student_notifications_api'),
]