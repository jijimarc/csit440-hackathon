from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('alumni', 'Alumni')], default='student')

    def __str__(self):
        return self.email or self.username
