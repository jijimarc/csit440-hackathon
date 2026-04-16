from django.contrib import admin
from .models import Document, Request, Completion, Payment

# Register your models here.
admin.site.register(Document)
admin.site.register(Request)
admin.site.register(Completion)
admin.site.register(Payment)