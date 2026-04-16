from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser, Customer, Student, Alumni

class UserRegistrationForm(UserCreationForm):
    fullname = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@cit.edu'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '09123456789'}))
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    # Customer Fields
    student_id_number = forms.CharField(max_length=50, label="School ID Number", widget=forms.TextInput(attrs={'placeholder': '12-3456-789'}))
    department = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'College of Computer Studies'}))
    
    # Role Selection
    USER_ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
    ]
    customer_status = forms.ChoiceField(choices=USER_ROLE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('fullname', 'email', 'contact_number')

    @transaction.atomic
    def save(self, commit=True):
        # 1. Save the base CustomUser
        user = super().save(commit=False)
        user.fullname = self.cleaned_data['fullname']
        user.email = self.cleaned_data['email']
        user.contact_number = self.cleaned_data['contact_number']
        user.user_type = 'CUSTOMER'
        
        if commit:
            user.save()
            
            # 2. Create the Customer profile linked to the User
            customer = Customer.objects.create(
                user=user,
                student_id_number=self.cleaned_data['student_id_number'],
                department=self.cleaned_data['department'],
                customer_status=self.cleaned_data['customer_status']
            )
            
            # 3. Create the specific Student or Alumni profile
            if self.cleaned_data['customer_status'] == 'STUDENT':
                # You can add more fields to the form and pass them here
                Student.objects.create(
                    customer=customer,
                    program="Pending Update", # Default or from form
                    year_level=1
                )
            else:
                Alumni.objects.create(
                    customer=customer,
                    year_of_graduation="2026-01-01", # Default or from form
                    personal_email=user.email
                )
        return user