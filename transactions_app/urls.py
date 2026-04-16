from django.urls import path
from . import views

app_name = 'transactions_app'

urlpatterns = [
    # Action Views (Handling Form Submissions silently in the background)
    path('submit-request/', views.submit_new_request, name='submit_request'),
    path('submit-payment/', views.submit_payment, name='submit_payment'),

    # Page Views (Rendering the HTML Templates for the user)
    path('history/', views.request_history, name='request_history'),
    path('track/', views.track_request, name='track_request'),
    path('payment/', views.payment_page, name='payment'),
    
    # Placeholders for remaining sidebar links (to prevent NoReverseMatch crashes)
    path('documents/', views.my_documents, name='documents'),
    path('detail/<int:pk>/', views.request_detail, name='request_detail'),
]