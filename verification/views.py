from django.shortcuts import render, get_object_or_404
from certificates.models import Certificate, VerificationLog


def verify(request, cert_id):
    """Public certificate verification page"""
    try:
        cert = Certificate.objects.get(id=cert_id)
        # Log verification
        VerificationLog.objects.create(
            certificate=cert,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            is_valid=True,
        )
        polygon_tx_url = ''
        if cert.tx_hash:
            polygon_tx_url = f"https://amoy.polygonscan.com/tx/{cert.tx_hash}"

        return render(request, 'verification/verify.html', {
            'cert': cert,
            'polygon_tx_url': polygon_tx_url,
            'verification_count': cert.verification_logs.count(),
        })
    except Certificate.DoesNotExist:
        return render(request, 'verification/not_found.html', {}, status=404)
