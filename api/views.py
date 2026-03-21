import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from accounts.models import APIKey
from certificates.models import Certificate


def _get_api_key(request):
    """Extract and validate API key from X-API-Key header."""
    raw = request.headers.get('X-Api-Key') or request.headers.get('X-API-Key') or ''
    if not raw:
        return None, JsonResponse({'valid': False, 'error': 'Missing X-API-Key header'}, status=401)
    try:
        api_key = APIKey.objects.select_related('organization').get(key=raw, is_active=True)
    except APIKey.DoesNotExist:
        return None, JsonResponse({'valid': False, 'error': 'Invalid or revoked API key'}, status=403)

    # Update usage stats
    api_key.last_used_at = timezone.now()
    api_key.total_calls += 1
    api_key.save(update_fields=['last_used_at', 'total_calls'])
    return api_key, None


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def verify_certificate(request):
    """
    POST /api/v1/verify/

    Headers:
        X-API-Key: hd_...

    Body (JSON):
        {
            "cert_hash": "0xabc...",
            "fields": {
                "name": "Rahul Sharma",
                "email": "rahul@example.com"
            }
        }

    Returns:
        { "valid": true/false, "reason": "...", "certificate_id": "..." }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response

    # Authenticate
    api_key, err = _get_api_key(request)
    if err:
        return _cors(err)

    # Parse body
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _cors(JsonResponse({'valid': False, 'error': 'Invalid JSON body'}, status=400))

    cert_hash = (body.get('cert_hash') or '').strip()
    submitted_fields = body.get('fields') or {}

    if not cert_hash:
        return _cors(JsonResponse({'valid': False, 'error': 'cert_hash is required'}, status=400))

    # Look up certificate by hash
    cert = Certificate.objects.filter(cert_hash=cert_hash).first()
    if not cert:
        return _cors(JsonResponse({
            'valid': False,
            'reason': 'No certificate found with this hash',
        }, status=404))

    # Check certificate status
    if cert.status == 'revoked':
        return _cors(JsonResponse({
            'valid': False,
            'reason': 'This certificate has been revoked',
        }))

    # Validate submitted fields against stored certificate data
    mismatches = []

    name = submitted_fields.get('name', '').strip().lower()
    if name and cert.recipient_name.strip().lower() != name:
        mismatches.append('name')

    email = submitted_fields.get('email', '').strip().lower()
    if email and cert.recipient_email.strip().lower() != email:
        mismatches.append('email')

    # Check any extra_data fields (e.g. roll_no, course, etc.)
    for field_key, field_val in submitted_fields.items():
        if field_key in ('name', 'email'):
            continue
        stored_val = cert.extra_data.get(field_key, '')
        if str(field_val).strip().lower() != str(stored_val).strip().lower():
            mismatches.append(field_key)

    if mismatches:
        return _cors(JsonResponse({
            'valid': False,
            'reason': f"Details do not match certificate: {', '.join(mismatches)}",
        }))

    return _cors(JsonResponse({
        'valid': True,
        'certificate_id': str(cert.id),
        'recipient': cert.recipient_name,
        'issued_at': cert.issued_at.strftime('%Y-%m-%d'),
        'organization': cert.organization.name,
    }))


def _cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'
    return response
