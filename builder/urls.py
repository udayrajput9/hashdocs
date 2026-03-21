from django.urls import path
from . import views

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('<uuid:pk>/', views.template_edit, name='template_edit'),
    path('<uuid:pk>/save/', views.template_save, name='template_save'),
    path('<uuid:pk>/delete/', views.template_delete, name='template_delete'),
    path('<uuid:pk>/generate/', views.bulk_generate_page, name='bulk_generate_page'),
    path('<uuid:pk>/bulk/', views.bulk_generate, name='bulk_generate'),
    path('cert/<uuid:cert_pk>/sign/', views.update_tx_hash, name='update_tx_hash'),
    path('gallery/', views.template_gallery, name='template_gallery'),
    path('gallery/use/<str:preset_id>/', views.template_use_preset, name='template_use_preset'),
]
