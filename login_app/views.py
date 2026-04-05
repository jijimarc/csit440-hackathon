from django.shortcuts import redirect, render
from django.contrib.auth import logout

# Create your views here.
def login_view(request):
    return render(request, 'login_app/login.html')

def forgot_password(request):
    return render(request, 'login_app/forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('login_app:login')    