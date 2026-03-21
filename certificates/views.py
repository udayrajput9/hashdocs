import json
import hashlib
import os
import uuid
import zipfile
import io
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from .models import CertificateTemplate, Certificate, VerificationLog
import qrcode
from PIL import Image, ImageDraw, ImageFont
import requests


@login_required
def dashboard(request):
    org = request.user
    templates = CertificateTemplate.objects.filter(organization=org)
    certificates = Certificate.objects.filter(organization=org)
    recent_certs = certificates[:10]
    stats = {
        'templates': templates.count(),
        'total': certificates.count(),
        'issued': certificates.filter(status='issued').count(),
        'pending': certificates.filter(status='pending').count(),
    }
    return render(request, 'dashboard/dashboard.html', {
        'stats': stats,
        'recent_certs': recent_certs,
        'templates': templates[:6],
    })


@login_required
def certificate_list(request):
    certificates = Certificate.objects.filter(organization=request.user)
    return render(request, 'dashboard/certificates.html', {'certificates': certificates})


@login_required
def certificate_detail(request, pk):
    cert = get_object_or_404(Certificate, id=pk, organization=request.user)
    return render(request, 'dashboard/certificate_detail.html', {'cert': cert})


@login_required
def update_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet = data.get('wallet_address', '')
        request.user.wallet_address = wallet
        request.user.save()
        return JsonResponse({'status': 'ok', 'wallet': wallet})
    return JsonResponse({'error': 'POST required'}, status=400)
