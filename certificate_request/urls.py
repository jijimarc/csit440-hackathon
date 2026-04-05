"""
URL configuration for certificate_request project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('login_app.urls', namespace="login_app")),
    path('dashboard/', include('dashboard_app.urls', namespace="dashboard_app")),
    path('register/', include('register_app.urls', namespace="register_app")),

    # TEMPORARY STUBS — replace with real apps when ready
    path('requests/', include('dashboard_app.stub_urls', namespace="certificate_request")),
]
