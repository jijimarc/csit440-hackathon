from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Document, Payment, Request, Completion
from django.shortcuts import render, get_object_or_404

@login_required
@transaction.atomic
def submit_new_request(request):
    if request.method == 'POST':
        # 1. Extract data from the modal form
        document_value = request.POST.get('document_type') # e.g., 'transcript', 'diploma'
        urgency = request.POST.get('urgency_level')
        purpose = request.POST.get('purpose_of_request')
        delivery = request.POST.get('delivery_mode')
        address = request.POST.get('shipping_address')

        # 2. Find the Document in the database
        # (Using icontains to match "transcript" to "Transcript of Records")
        try:
            document = Document.objects.filter(doc_name__icontains=document_value).first()
            if not document:
                raise ValueError("Document not found in database.")
        except Exception as e:
            messages.error(request, "Error finding that document type. Please try again.")
            return redirect('dashboard_app:dashboard')

        # 3. Calculate the total fee
        total_fee = document.standard_fee
        if urgency == 'RUSH':
            total_fee += document.rush_fee

        try:
            # 4. Create the Request record
            new_request = Request.objects.create(
                user=request.user,
                document=document,
                urgency_level=urgency,
                purpose_of_request=purpose,
                total_fee=total_fee,
                status='PENDING'
            )

            # 5. Create the Completion record linked to the Request
            Completion.objects.create(
                request=new_request,
                delivery_mode=delivery,
                # Only save the address if they chose courier delivery
                shipping_address=address if delivery == 'Courier' else None 
            )

            messages.success(request, f"Successfully requested {document.doc_name}!")
            
        except Exception as e:
            messages.error(request, "An error occurred while saving your request.")
            
        return redirect('dashboard_app:dashboard')

    # If someone tries to visit the URL directly via GET, kick them back to the dashboard
    return redirect('dashboard_app:dashboard')

@login_required
def request_history(request):
    # Get all requests for this user, newest first
    user_requests = Request.objects.filter(user=request.user).order_by('-date_requested')
    return render(request, 'my_requests.html', {'requests': user_requests})

@login_required
def payment_page(request):
    # Only show requests that haven't been paid/processed yet
    pending = Request.objects.filter(user=request.user, status='PENDING')
    return render(request, 'payments.html', {'pending_requests': pending})

@login_required
def track_request(request):
    # Show requests that are currently active (exclude completed or rejected ones if you want)
    active = Request.objects.filter(user=request.user).exclude(status='REJECTED')
    return render(request, 'track_request.html', {'active_requests': active})

@login_required
def submit_payment(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        ref_number = request.POST.get('reference_number')
        proof_img = request.FILES.get('proof_of_payment') # Getting the uploaded image
        
        try:
            req_obj = Request.objects.get(id=request_id, user=request.user)
            
            # Create the Payment record
            Payment.objects.create(
                request=req_obj,
                user=request.user,
                reference_number=ref_number,
                proof_of_payment=proof_img
            )
            
            # Optional: Automatically update the request status to 'VERIFIED' or 'PROCESSING' here
            # req_obj.status = 'VERIFIED'
            # req_obj.save()
            
            messages.success(request, "Payment submitted successfully! Please wait for verification.")
        except Exception as e:
            messages.error(request, "An error occurred submitting your payment.")
            
    return redirect('transactions_app:payment')

# --- Temporary Placeholders for the remaining URLs ---
@login_required
def my_documents(request):
    return render(request, 'customer_dashboard.html') # Placeholder redirect

@login_required
def request_detail(request, pk):
    return render(request, 'customer_dashboard.html') # Placeholder redirect