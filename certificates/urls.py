from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/<uuid:pk>/', views.certificate_detail, name='certificate_detail'),
    path('update-wallet/', views.update_wallet, name='update_wallet'),
]
