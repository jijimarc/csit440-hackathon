from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Since CustomUser handles all fields, we just call save()
            user = form.save()
            
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}! You can now log in.')
            return redirect('login_app:login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register_app/register.html', {
        'form': form
    })
