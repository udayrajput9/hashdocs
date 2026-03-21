from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Organization, APIKey
from .forms import RegisterForm, LoginForm, ProfileForm


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to HashDocs, {user.name}! Your organization is registered.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def update_wallet(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            wallet_address = data.get('wallet_address')
            if wallet_address:
                request.user.wallet_address = wallet_address
                request.user.save()
                return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def api_keys(request):
    keys = request.user.api_keys.all()
    return render(request, 'accounts/api_keys.html', {'api_keys': keys})


@login_required
def api_keys_generate(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'API Key name is required.')
            return redirect('api_keys')
        
        # Limit to 10 keys per org
        if request.user.api_keys.filter(is_active=True).count() >= 10:
            messages.error(request, 'You can only have up to 10 active API keys.')
            return redirect('api_keys')

        APIKey.objects.create(organization=request.user, name=name)
        messages.success(request, f'API Key "{name}" generated successfully.')
    return redirect('api_keys')


@login_required
def api_keys_revoke(request, pk):
    if request.method == 'POST':
        key = get_object_or_404(APIKey, id=pk, organization=request.user)
        key.is_active = False
        key.save()
        messages.info(request, f'API Key "{key.name}" has been revoked.')
    return redirect('api_keys')
