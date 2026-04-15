from django.shortcuts import render
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'dashboard_app/dashboard.html')

def student_dashboard_base(request):
    return render(request, 'dashboard_app/student_dashboard_base.html')

def customer_dashboard(request):
    return render(request, 'dashboard_app/customer_dashboard.html')

def staff_dashboard(request):
    return render(request, 'dashboard_app/staff_dashboard.html')

def profile(request):
    return render(request, 'dashboard_app/profile.html')

def help(request):
    return render(request, 'dashboard_app/help.html')

def student_notifications_api(request):
    return JsonResponse({'notifications': []})

def clear_student_notifications_api(request):
    return JsonResponse({'status': 'ok'})