"""
Builder App Views - Core certificate generation engine
Handles: Template CRUD, Canva-style builder, CSV bulk generation
"""
import json
import hashlib
import os
import io
import zipfile
import uuid as uuid_lib
import base64
import math
import pandas as pd
import qrcode
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image, ImageDraw, ImageFont, ImageColor
from certificates.models import CertificateTemplate, Certificate
from .presets import TEMPLATE_PRESETS
from .utils_ipfs import upload_to_ipfs


# ─── Template Management ────────────────────────────────────────────────────

@login_required
def template_list(request):
    templates = CertificateTemplate.objects.filter(organization=request.user)
    return render(request, 'builder/template_list.html', {'templates': templates})


@login_required
def template_create(request):
    """Create a new blank template → redirect to editor"""
    template = CertificateTemplate.objects.create(
        organization=request.user,
        name='Untitled Certificate',
        canvas_json={
            'version': '5.3.0',
            'objects': [
                {"type":"i-text", "text":"Certificate Title", "left":500, "top":150, "originX":"center", "fontSize":48, "fontWeight":"bold", "fill":"#1a1a2e", "fontFamily":"Inter, Arial"},
                {"type":"i-text", "text":"{{name}}", "left":500, "top":280, "originX":"center", "fontSize":56, "fontWeight":"bold", "fill":"#2563eb", "fontFamily":"Inter, Arial"},
                {"type":"i-text", "text":"For completing {{course}}", "left":500, "top":400, "originX":"center", "fontSize":24, "fill":"#64748b", "fontFamily":"Inter, Arial"},
                {"type":"i-text", "text":"{{date}}", "left":300, "top":550, "originX":"center", "fontSize":18, "fill":"#4b5563", "fontFamily":"Inter, Arial"},
                {"type":"i-text", "text":"{{organization}}", "left":700, "top":550, "originX":"center", "fontSize":18, "fill":"#4b5563", "fontWeight":"bold", "fontFamily":"Inter, Arial"},
            ],
            'background': '#ffffff'
        }
    )
    return redirect('template_edit', pk=template.id)


@login_required
def template_edit(request, pk):
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    return render(request, 'builder/editor.html', {
        'template': template,
        'canvas_json': json.dumps(template.canvas_json),
    })


@login_required
def template_delete(request, pk):
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted.')
    return redirect('template_list')


@login_required
def template_gallery(request):
    """Display the 10 pre-designed JSON presets"""
    return render(request, 'builder/template_gallery.html', {'presets': TEMPLATE_PRESETS})


@login_required
def template_use_preset(request, preset_id):
    """Create a new template from a preset and redirect to editor"""
    preset = next((p for p in TEMPLATE_PRESETS if p['id'] == preset_id), None)
    if not preset:
        messages.error(request, 'Preset not found.')
        return redirect('template_gallery')
        
    template = CertificateTemplate.objects.create(
        organization=request.user,
        name=preset['name'],
        category=preset['category'],
        canvas_json=preset['canvas_json'],
        background_color=preset['canvas_json'].get('background', '#ffffff')
    )
    messages.success(request, f'Template "{preset["name"]}" loaded. You can now edit it.')
    return redirect('template_edit', pk=template.id)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def template_save(request, pk):
    """Save canvas JSON from the editor"""
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    try:
        data = json.loads(request.body)
        template.name = data.get('name', template.name)
        template.canvas_json = data.get('canvas_json', template.canvas_json)
        template.background_color = data.get('background', '#ffffff')

        # Save thumbnail if provided
        thumbnail_b64 = data.get('thumbnail_base64')
        if thumbnail_b64 and ',' in thumbnail_b64:
            header, img_data = thumbnail_b64.split(',', 1)
            img_bytes = base64.b64decode(img_data)
            template.thumbnail.save(f'thumb_{pk}.png', ContentFile(img_bytes), save=False)

        template.save()
        return JsonResponse({'status': 'saved', 'id': str(template.id), 'name': template.name})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ─── CSV Bulk Generation ─────────────────────────────────────────────────────

@login_required
def bulk_generate_page(request, pk):
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    recent = Certificate.objects.filter(
        template=template, organization=request.user
    )[:20]
    return render(request, 'builder/bulk_generate.html', {
        'template': template,
        'recent': recent,
    })


@login_required
@require_http_methods(["POST"])
def bulk_generate(request, pk):
    return JsonResponse({'error': 'Deprecated. Use bulk/init/ instead.'}, status=400)

@login_required
@require_http_methods(["POST"])
def bulk_generate_init(request, pk):
    """
    Step 1:
    Parse CSV. For each row: render BASE image (no QR) -> hash it -> save to DB as 'pending'.
    Returns JSON list of generated hashes that the frontend needs to sign.
    """
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        return JsonResponse({'error': 'Please upload a CSV file.'}, status=400)

    try:
        df = pd.read_csv(csv_file)
        df.columns = [c.strip().lower() for c in df.columns]
    except Exception as e:
        return JsonResponse({'error': f'Invalid CSV file: {e}'}, status=400)

    required_name_col = None
    for col in ['name', 'recipient_name', 'full_name', 'student_name']:
        if col in df.columns:
            required_name_col = col
            break

    if not required_name_col:
        return JsonResponse({'error': "CSV must have a 'name' column."}, status=400)

    generated_certs = []
    errors = []

    for idx, row in df.iterrows():
        row_dict = {k: (str(v) if pd.notnull(v) else '') for k, v in row.to_dict().items()}
        recipient_name = row_dict.get(required_name_col, f'Recipient {idx+1}').strip()
        recipient_email = row_dict.get('email', '').strip()

        cert_id = uuid_lib.uuid4()

        try:
            # Render Base Image (No QR)
            cert_image = _render_certificate(
                template=template,
                recipient_name=recipient_name,
                row_data=row_dict,
                cert_id=str(cert_id),
                org_name=request.user.name
            )

            img_bytes = BytesIO()
            cert_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Hash Base Image
            cert_hash = '0x' + hashlib.sha256(img_bytes.read()).hexdigest()
            img_bytes.seek(0)

            # Create Certificate Record in 'pending' state
            verify_url = f"{request.scheme}://{request.get_host()}/verify/{cert_id}/"
            cert = Certificate(
                id=cert_id,
                template=template,
                organization=request.user,
                recipient_name=recipient_name,
                recipient_email=recipient_email,
                extra_data=row_dict,
                cert_hash=cert_hash,
                verification_url=verify_url,
                status='pending',
            )
            safe_name = recipient_name.replace(' ', '_').replace('/', '_')
            cert_file_name = f"cert_{safe_name}_{cert_id}.png"
            cert.certificate_image.save(cert_file_name, ContentFile(img_bytes.getvalue()), save=False)
            cert.save()

            generated_certs.append({
                'id': str(cert_id),
                'hash': cert_hash,
                'name': recipient_name
            })

        except Exception as e:
            errors.append(f"Row {idx+1} ({recipient_name}): {e}")
            continue

    return JsonResponse({
        'status': 'ok',
        'certificates': generated_certs,
        'errors': errors
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def bulk_generate_finalize(request, cert_pk):
    """
    Step 2:
    Receives tx_hash for a pending cert.
    Generates QR code (with verify URL).
    Composites QR onto Base Image.
    Uploads Final Image to IPFS.
    Saves and marks as 'issued'.
    """
    try:
        data = json.loads(request.body)
        tx_hash = data.get('tx_hash', '').strip()
        signature = data.get('signature', '').strip()
        
        cert = get_object_or_404(Certificate, id=cert_pk, organization=request.user, status='pending')
        
        # We need the base image
        if not cert.certificate_image:
            return JsonResponse({'error': 'Base image not found'}, status=400)
            
        base_img = Image.open(cert.certificate_image).convert('RGBA')
        
        # Generate QR Code
        qr_img = _generate_qr(cert.verification_url)
        
        # Composite
        final_img = _composite_qr(base_img, qr_img)
        final_bytes = BytesIO()
        final_img.save(final_bytes, format='PNG')
        file_data = final_bytes.getvalue()
        
        # Upload to IPFS
        filename = f"certificate_{cert.id}.png"
        ipfs_cid, ipfs_url = upload_to_ipfs(file_data, filename)
        
        # Update DB
        cert.tx_hash = tx_hash
        cert.wallet_signature = signature
        cert.ipfs_cid = ipfs_cid
        cert.ipfs_url = ipfs_url
        cert.status = 'issued'
        
        # Overwrite the base image with the final composite image
        cert.certificate_image.save(filename, ContentFile(file_data), save=False)
        
        # Save QR code separately
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        cert.qr_code.save(f"qr_{cert.id}.png", ContentFile(qr_bytes.getvalue()), save=False)
        
        cert.save()
        
        return JsonResponse({'status': 'ok', 'ipfs_cid': ipfs_cid, 'tx_hash': tx_hash})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET", "POST"])
def bulk_download_zip(request, pk):
    """
    Step 3: Download ZIP of requested cert IDs
    """
    template = get_object_or_404(CertificateTemplate, id=pk, organization=request.user)
    
    cert_ids = []
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cert_ids = data.get('cert_ids', [])
        except:
            pass
    elif request.method == 'GET':
        cert_ids = request.GET.get('ids', '').split(',')
        
    cert_ids = [c for c in cert_ids if c]
    
    certs = Certificate.objects.filter(
        id__in=cert_ids, 
        organization=request.user, 
        status='issued'
    )
    
    if not certs.exists():
        messages.error(request, 'No issued certificates found to download.')
        return redirect('bulk_generate_page', pk=pk)
        
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for cert in certs:
            if cert.certificate_image:
                try:
                    file_name = f"{cert.recipient_name.replace(' ', '_')}_{cert.id}.png"
                    zf.writestr(file_name, cert.certificate_image.read())
                except:
                    pass
                    
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="certificates_{template.name}.zip"'
    return response
# (Old bulk_generate execution body removed, replaced by async functions above)


# ─── Certificate Rendering Engine ───────────────────────────────────────────

def _parse_color(color_str, opacity=1.0):
    """Convert CSS color string to RGBA tuple. Handles #hex, rgb(), rgba(), named colors."""
    if not color_str or color_str in ('transparent', 'none', ''):
        return (0, 0, 0, 0)
    try:
        color_str = str(color_str).strip()
        alpha = max(0, min(255, int(float(opacity) * 255)))

        if color_str.startswith('#'):
            h = color_str.lstrip('#')
            if len(h) == 3:
                h = ''.join(c * 2 for c in h)
            if len(h) == 8:  # #RRGGBBAA
                r, g, b, a = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), int(h[6:8],16)
                return (r, g, b, min(alpha, a))
            r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            return (r, g, b, alpha)

        if 'rgb' in color_str:
            nums = color_str.replace('rgba(','').replace('rgb(','').replace(')','')
            parts = [p.strip() for p in nums.split(',')]
            r, g, b = int(float(parts[0])), int(float(parts[1])), int(float(parts[2]))
            a = int(float(parts[3]) * 255) if len(parts) > 3 else alpha
            return (r, g, b, min(alpha, a))

        # Named CSS colors
        rgb = ImageColor.getrgb(color_str)
        return (rgb[0], rgb[1], rgb[2], alpha)
    except Exception:
        return (0, 0, 0, int(float(opacity) * 255))


def _get_font(size, bold=False):
    """Try multiple font paths; fall back to Pillow default."""
    size = max(8, int(size))
    font_dir = os.path.join(settings.BASE_DIR, 'static', 'fonts')

    candidates = [
        # Project fonts
        os.path.join(font_dir, 'Inter-Bold.ttf' if bold else 'Inter-Regular.ttf'),
        # Windows system fonts
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/calibrib.ttf' if bold else 'C:/Windows/Fonts/calibri.ttf',
        'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/tahoma.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # Pillow 10+ supports size argument
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def _render_certificate(template, recipient_name, row_data, cert_id, org_name):
    """
    Render a certificate PNG from Fabric.js canvas JSON using Pillow.
    Supports: textbox, text, i-text, rect, circle, ellipse, line, image (base64)
    Dynamic fields: {{name}}, {{date}}, {{course}}, {{cert_id}}, {{organization}}, plus any CSV column.
    """
    W = template.width or 1000
    H = template.height or 700

    canvas_data = template.canvas_json

    # ── Background ──
    bg_color = canvas_data.get('background', template.background_color or '#ffffff')
    img = Image.new('RGBA', (W, H), _parse_color(bg_color))
    draw = ImageDraw.Draw(img)
    objects = canvas_data.get('objects', [])

    # ── Build field replacement map ──
    row_data = {k: (str(v) if v else '') for k, v in row_data.items()}
    replacements = {
        '{{name}}':           recipient_name,
        '{{recipient_name}}': recipient_name,
        '{{organization}}':   org_name,
        '{{cert_id}}':        cert_id[:8].upper(),
        '{{date}}':           row_data.get('date', ''),
        '{{course}}':         row_data.get('course', row_data.get('subject', '')),
        '{{grade}}':          row_data.get('grade', ''),
        '{{score}}':          row_data.get('score', ''),
        '{{email}}':          row_data.get('email', ''),
    }
    # Add every CSV column as {{column_name}}
    for k, v in row_data.items():
        key = '{{' + k + '}}'
        if key not in replacements:
            replacements[key] = v

    # Smart label map: plain text labels users might type → value
    # Only used when text is an EXACT match (case-insensitive) so "My Name" is NOT replaced
    label_map = {
        'name':             recipient_name,
        'student name':     recipient_name,
        'recipient name':   recipient_name,
        'recipient':        recipient_name,
        'full name':        recipient_name,
        'course':           row_data.get('course', row_data.get('subject', '')),
        'subject':          row_data.get('subject', row_data.get('course', '')),
        'date':             row_data.get('date', ''),
        'issue date':       row_data.get('date', ''),
        'grade':            row_data.get('grade', ''),
        'score':            row_data.get('score', ''),
        'email':            row_data.get('email', ''),
        'organization':     org_name,
        'org':              org_name,
        'cert id':          cert_id[:8].upper(),
        'certificate id':   cert_id[:8].upper(),
        'id':               cert_id[:8].upper(),
    }
    # Also add any CSV column name as a plain-text label
    for k, v in row_data.items():
        if k not in label_map:
            label_map[k.lower()] = v

    def replace_fields(text):
        # Pass 1: Replace {{placeholder}} syntax
        result = text
        for k, v in replacements.items():
            result = result.replace(k, v)

        # Pass 2: If the ENTIRE text exactly equals a known label (case-insensitive),
        # replace it with the corresponding value.
        # This handles the case where user typed "Name" instead of "{{name}}"
        if result == text:  # nothing was replaced in pass 1
            stripped = text.strip().lower()
            if stripped in label_map and label_map[stripped]:
                result = label_map[stripped]

        return result

    # ── Render each Fabric.js object ──
    for obj in objects:
        obj_type = obj.get('type', '').lower()
        if not obj_type or not obj.get('visible', True):
            continue

        opacity  = float(obj.get('opacity', 1))
        scale_x  = float(obj.get('scaleX', 1))
        scale_y  = float(obj.get('scaleY', 1))
        left     = float(obj.get('left', 0))
        top      = float(obj.get('top',  0))
        angle    = float(obj.get('angle', 0))
        fill_str = obj.get('fill', '#000000') or '#000000'
        stroke_s = obj.get('stroke', '') or ''

        # ── TEXT ──────────────────────────────────────
        if obj_type in ('textbox', 'text', 'i-text'):
            raw_text   = obj.get('text', '')
            text       = replace_fields(raw_text)
            font_size  = max(8, int(float(obj.get('fontSize', 22)) * min(scale_x, scale_y)))
            is_bold    = str(obj.get('fontWeight', '')).lower() in ('bold', '700', '800', '900')
            font       = _get_font(font_size, bold=is_bold)
            fill_color = _parse_color(fill_str, opacity)
            obj_w      = max(10, int(float(obj.get('width', 300)) * scale_x))
            text_align = obj.get('textAlign', 'left')

            try:
                bbox   = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
            except Exception:
                text_w = len(text) * (font_size // 2)

            draw_x = left
            if text_align == 'center':
                draw_x = left + (obj_w - text_w) // 2
            elif text_align == 'right':
                draw_x = left + obj_w - text_w

            draw.text((draw_x, top), text, fill=fill_color[:3], font=font)

        # ── RECT ──────────────────────────────────────
        elif obj_type == 'rect':
            w = max(1, int(float(obj.get('width',  100)) * scale_x))
            h = max(1, int(float(obj.get('height',  50)) * scale_y))
            fill_color   = _parse_color(fill_str, opacity)
            stroke_color = _parse_color(stroke_s, opacity) if stroke_s else None
            stroke_w     = int(float(obj.get('strokeWidth', 0)))

            if fill_str and fill_str not in ('transparent', 'none'):
                draw.rectangle([left, top, left+w, top+h], fill=fill_color[:3])
            if stroke_color and stroke_w > 0:
                draw.rectangle([left, top, left+w, top+h],
                                outline=stroke_color[:3], width=stroke_w)

        # ── CIRCLE / ELLIPSE ──────────────────────────
        elif obj_type in ('circle', 'ellipse'):
            r  = float(obj.get('radius', 50))
            rx = float(obj.get('rx', r)) * scale_x
            ry = float(obj.get('ry', r)) * scale_y
            if obj_type == 'circle':
                rx = ry = r * scale_x
            fill_color = _parse_color(fill_str, opacity)
            draw.ellipse([left, top, left + rx*2, top + ry*2], fill=fill_color[:3])

        # ── LINE ──────────────────────────────────────
        elif obj_type == 'line':
            x1 = float(obj.get('x1', 0))
            y1 = float(obj.get('y1', 0))
            x2 = float(obj.get('x2', float(obj.get('width', 200))))
            y2 = float(obj.get('y2', 0))
            stroke_color = _parse_color(stroke_s or fill_str, opacity)
            stroke_w     = max(1, int(float(obj.get('strokeWidth', 2))))
            # Fabric stores line coords relative to object center
            cx = left  # left is already the placed position
            cy = top
            draw.line([cx+x1, cy+y1, cx+x2, cy+y2],
                      fill=stroke_color[:3], width=stroke_w)

        # ── IMAGE ─────────────────────────────────────
        elif obj_type == 'image':
            src = obj.get('src', '')
            if not src:
                continue
            try:
                if src.startswith('data:'):
                    # Base64 data URL: "data:image/png;base64,<data>"
                    if ',' not in src:
                        continue
                    _, b64_data = src.split(',', 1)
                    raw = base64.b64decode(b64_data)
                    elem_img = Image.open(BytesIO(raw)).convert('RGBA')
                else:
                    # Skip remote URLs (would need requests library + network)
                    continue

                # Apply scale
                orig_w, orig_h = elem_img.size
                new_w = max(1, int(orig_w * scale_x))
                new_h = max(1, int(orig_h * scale_y))
                elem_img = elem_img.resize((new_w, new_h), Image.LANCZOS)

                # Apply rotation
                if angle != 0:
                    elem_img = elem_img.rotate(-angle, expand=True, resample=Image.BICUBIC)

                # Apply opacity
                if opacity < 1.0:
                    r2, g2, b2, a2 = elem_img.split()
                    a2 = a2.point(lambda x: int(x * opacity))
                    elem_img.putalpha(a2)

                # Paste onto main canvas (using alpha mask)
                paste_pos = (int(left), int(top))
                if elem_img.mode == 'RGBA':
                    img.paste(elem_img, paste_pos, elem_img)
                else:
                    img.paste(elem_img, paste_pos)

            except Exception as e:
                print(f"[HashDocs] Image render skipped: {e}")
                continue

    # Convert RGBA → RGB (white background merge)
    background = Image.new('RGB', img.size, (255, 255, 255))
    if img.mode == 'RGBA':
        background.paste(img, mask=img.split()[3])
    else:
        background.paste(img)
    return background


def _generate_qr(url):
    """Generate QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='#1a1a2e', back_color='white')
    return qr_img.convert('RGB')


def _composite_qr(cert_img, qr_img):
    """Paste QR code onto bottom-right of certificate"""
    cert_img = cert_img.copy()
    qr_size = min(cert_img.width // 6, 120)
    qr_resized = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    margin = 20
    pos = (cert_img.width - qr_size - margin, cert_img.height - qr_size - margin)
    cert_img.paste(qr_resized, pos)
    return cert_img


# ─── API Endpoints ───────────────────────────────────────────────────────────

@login_required
def update_tx_hash(request, cert_pk):
    """Called from frontend after MetaMask signing"""
    if request.method == 'POST':
        data = json.loads(request.body)
        cert = get_object_or_404(Certificate, id=cert_pk, organization=request.user)
        cert.tx_hash = data.get('tx_hash', '')
        cert.wallet_signature = data.get('signature', '')
        cert.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST required'}, status=400)
