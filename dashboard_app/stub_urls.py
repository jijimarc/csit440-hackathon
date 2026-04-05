from django.urls import path
from django.http import HttpResponse

app_name = "certificate_request"

def stub(request, *args, **kwargs):
    return HttpResponse("Coming soon.")

urlpatterns = [
    path('new/', stub, name='new_request'),
    path('history/', stub, name='request_history'),
    path('track/', stub, name='track_request'),
    path('payment/', stub, name='payment'),
    path('documents/', stub, name='documents'),
    path('detail/<int:pk>/', stub, name='request_detail'),
]