from django.contrib import admin
from .models import CustomUser, Customer, Student, Alumni, Staff

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Student)
admin.site.register(Alumni)
admin.site.register(Staff)