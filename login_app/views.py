from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Try to authenticate with username first
        user = authenticate(request, username=identifier, password=password)

        # If it fails, check if the identifier is an email and try to find the user
        if user is None:
            try:
                user_by_email = User.objects.get(email=identifier)
                user = authenticate(request, username=user_by_email.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard_app:dashboard')
        else:
            messages.error(request, "Invalid email/username or password.")
            return render(request, 'login_app/login.html')
            
    return render(request, 'login_app/login.html')

def forgot_password(request):
    return render(request, 'login_app/forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('login_app:login')    