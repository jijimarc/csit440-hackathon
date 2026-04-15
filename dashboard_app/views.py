from django.shortcuts import render
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'dashboard.html')

def student_dashboard_base(request):
    return render(request, 'student_dashboard_base.html')

def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

def profile(request):
    return render(request, 'profile.html')

def help(request):
    return render(request, 'help.html')

def student_notifications_api(request):
    return JsonResponse({'notifications': []})

def clear_student_notifications_api(request):
    return JsonResponse({'status': 'ok'})