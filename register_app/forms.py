from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': '09xx xxx xxxx'}))
    user_type = forms.ChoiceField(choices=[('student', 'Student'), ('alumni', 'Alumni')], widget=forms.Select())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'user_type')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.contact_number = self.cleaned_data.get('contact_number')
        user.user_type = self.cleaned_data.get('user_type')
        if commit:
            user.save()
        return user
