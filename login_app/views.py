from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'login_app/login.html')

def forgot_password(request):
    return render(request, 'login_app/forgot_password.html')

    