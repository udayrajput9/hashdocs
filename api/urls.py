from django.urls import path
from . import views

urlpatterns = [
    path('v1/verify/', views.verify_certificate, name='api_verify'),
]
