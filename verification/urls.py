from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:cert_id>/', views.verify, name='verify_certificate'),
]
