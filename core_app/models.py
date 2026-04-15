import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Overriding the default ID to be a UUID as specified in the ERD
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    USER_TYPE_CHOICES = [
        ('STAFF', 'Staff'),
        ('CUSTOMER', 'Customer'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='CUSTOMER')

    def __str__(self):
        return self.fullname or self.email or self.username


class Staff(models.Model):
    # OneToOneField acts as both Primary Key and Foreign Key to User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    employee_id_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=100)
    digital_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return f"Staff: {self.user.fullname}"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    student_id_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    
    STATUS_CHOICES = [
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
    ]
    customer_status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Customer: {self.student_id_number}"


class Student(models.Model):
    # Links directly to Customer, extending its data
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    program = models.CharField(max_length=100)
    year_level = models.IntegerField()
    is_regular = models.BooleanField(default=True)

    def __str__(self):
        return f"Student: {self.customer.user.fullname}"


class Alumni(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    year_of_graduation = models.DateField()
    valid_personal_id = models.ImageField(upload_to='alumni_ids/', blank=True, null=True)
    personal_email = models.EmailField()

    def __str__(self):
        return f"Alumni: {self.customer.user.fullname}"