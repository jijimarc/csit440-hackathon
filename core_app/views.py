from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                user_by_email = User.objects.get(email=identifier)
                user = authenticate(request, username=user_by_email.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard_app:customer_dashboard')
        else:
            messages.error(request, "Invalid email/username or password.")
            return render(request, 'login.html')
            
    return render(request, 'login.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('core:login') 

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}! You can now log in.')
            return redirect('core:login')
        else:
            # ADD THIS LINE TO DEBUG:
            print("FORM ERRORS:", form.errors)
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register.html', {
        'form': form
    })