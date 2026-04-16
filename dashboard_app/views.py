from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# ROUTER VIEW
@login_required
def dashboard_router(request):
    if hasattr(request.user, 'user_type') and request.user.user_type == 'STAFF':
        return redirect('dashboard_app:staff_dashboard')
    
    return redirect('dashboard_app:customer_dashboard')


# DASHBOARD VIEWS
@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')


# ACCOUNT VIEWS
@login_required
def profile(request):
    if request.method == 'POST':
        new_contact_number = request.POST.get('contact_number')
        if new_contact_number:
            request.user.contact_number = new_contact_number
            request.user.save()
            from django.contrib import messages
            messages.success(request, 'Contact number updated successfully.')
            return redirect('dashboard_app:profile')

    return render(request, 'profile.html')

@login_required
def help(request):
    return render(request, 'help.html')


# API VIEWS (Used by JavaScript)
@login_required
def student_notifications_api(request):
    return JsonResponse({'notifications': []})

@login_required
def clear_student_notifications_api(request):
    return JsonResponse({'status': 'ok'})