from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from core_app.password_validators import validate_password_strength, validate_password_match

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
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validation
        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'Please fill in all password fields.')
        elif not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
        elif old_password == new_password:
            messages.error(request, 'New password must be different from the current password.')
        else:
            # Validate password strength
            strength_check = validate_password_strength(new_password)
            if not strength_check['is_valid']:
                for error in strength_check['errors']:
                    messages.error(request, error)
            else:
                # Validate passwords match
                match_check = validate_password_match(new_password, confirm_password)
                if not match_check['is_valid']:
                    messages.error(request, match_check['error'])
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('dashboard_app:profile')

    return render(request, 'change_password.html')

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