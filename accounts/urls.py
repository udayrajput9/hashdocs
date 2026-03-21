from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update-wallet/', views.update_wallet, name='update_wallet'),
    path('api-keys/', views.api_keys, name='api_keys'),
    path('api-keys/generate/', views.api_keys_generate, name='api_keys_generate'),
    path('api-keys/<uuid:pk>/revoke/', views.api_keys_revoke, name='api_keys_revoke'),
]
