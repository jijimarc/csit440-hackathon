from django.db import models
from django.conf import settings

# DOCUMENT MODEL
class Document(models.Model):
    # doc_id is automatically created by Django as 'id' (Primary Key)
    doc_name = models.CharField(max_length=255)
    description = models.TextField()
    standard_fee = models.DecimalField(max_digits=10, decimal_places=2)
    rush_fee = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(help_text="List of requirements needed for this document")
    
    AVAILABILITY_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
    ]
    availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='AVAILABLE')

    def __str__(self):
        return self.doc_name


# REQUEST MODEL
class Request(models.Model):
    # request_id is automatically created by Django as 'id' (Primary Key)
    
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    document = models.ForeignKey(Document, on_delete=models.RESTRICT) # RESTRICT prevents deleting a doc if requests exist
    
    # Staff processing the request (Linked using string reference to avoid circular imports)
    processed_by = models.ForeignKey('core_app.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requests')

    # Request Details
    date_requested = models.DateField(auto_now_add=True)
    
    URGENCY_CHOICES = [
        ('STANDARD', 'Standard'),
        ('RUSH', 'Rush'),
    ]
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='STANDARD')
    
    purpose_of_request = models.TextField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Request #{self.id} - {self.user.fullname} ({self.document.doc_name})"


# COMPLETION MODEL
class Completion(models.Model):
    # completion_id is automatically created by Django as 'id' (Primary Key)
    
    # OneToOne because one request has exactly one completion record
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='completion_details')
    
    DELIVERY_CHOICES = [
        ('PICKUP', 'Pick-up'),
        ('COURIER', 'Courier Delivery'),
    ]
    delivery_mode = models.CharField(max_length=15, choices=DELIVERY_CHOICES)
    
    # Nullable fields because they might not apply (e.g., if picking up, no shipping address is needed)
    shipping_address = models.TextField(blank=True, null=True)
    courier_partner = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    estimated_delivery_date = models.DateField(blank=True, null=True)
    date_claimed = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Completion Details for Request #{self.request.id}"


# PAYMENT MODEL
class Payment(models.Model):
    # payment_id is automatically created by Django as 'id' (Primary Key)
    
    # Foreign Keys
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='payment_details')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Staff verifying the payment
    verified_by = models.ForeignKey('core_app.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')

    # Payment Details
    reference_number = models.CharField(max_length=100, unique=True)
    proof_of_payment = models.ImageField(upload_to='payments/proofs/')
    verification_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Request #{self.request.id} - Ref: {self.reference_number}"