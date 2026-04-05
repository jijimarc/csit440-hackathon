from django.shortcuts import render
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'dashboard_app/dashboard.html')

def profile(request):
    return render(request, 'dashboard_app/profile.html')

def help(request):
    return render(request, 'dashboard_app/help.html')

def student_notifications_api(request):
    return JsonResponse({'notifications': []})

def clear_student_notifications_api(request):
    return JsonResponse({'status': 'ok'})