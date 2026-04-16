from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView  # Import this

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Send base URL to the login page
    path('', RedirectView.as_view(pattern_name='core:login', permanent=False)), 
    
    path('auth/', include('core_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
    path('transactions/', include('transactions_app.urls')),
]