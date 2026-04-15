from django.urls import path
from . import views

app_name = "dashboard_app"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('student/dashboard', views.student_dashboard_base, name='student_dashboard_base'),
    path('customer/dashboard', views.customer_dashboard, name='customer_dashboard'),
    path('staff/dashboard', views.staff_dashboard, name='staff_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('help/', views.help, name='help'),
    path('api/notifications/', views.student_notifications_api, name='student_notifications_api'),
    path('api/notifications/clear/', views.clear_student_notifications_api, name='clear_student_notifications_api'),
]