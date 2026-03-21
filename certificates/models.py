from django.db import models
from django.conf import settings
import uuid


class CertificateTemplate(models.Model):
    CATEGORIES = [
        ('academic', 'Academic'),
        ('professional', 'Professional'),
        ('completion', 'Completion'),
        ('achievement', 'Achievement'),
        ('participation', 'Participation'),
        ('custom', 'Custom'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='templates'
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='custom')
    canvas_json = models.JSONField(default=dict, help_text='Fabric.js canvas JSON data')
    background_color = models.CharField(max_length=7, default='#ffffff')
    thumbnail = models.ImageField(upload_to='template_thumbnails/', blank=True, null=True)
    width = models.IntegerField(default=1000)
    height = models.IntegerField(default=700)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} - {self.organization.name}"

    @property
    def certificate_count(self):
        return self.certificates.count()


class Certificate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('issued', 'Issued'),
        ('revoked', 'Revoked'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        CertificateTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='certificates'
    )
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField(blank=True)
    extra_data = models.JSONField(default=dict, help_text='Additional CSV fields used in template')

    # Storage
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    ipfs_cid = models.CharField(max_length=255, blank=True, help_text='IPFS Content ID')
    ipfs_url = models.URLField(blank=True)

    # Blockchain
    cert_hash = models.CharField(max_length=66, blank=True, help_text='SHA-256 hash of certificate')
    tx_hash = models.CharField(max_length=66, blank=True, help_text='Blockchain transaction hash')
    wallet_signature = models.TextField(blank=True, help_text='MetaMask signature of hash')

    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    verification_url = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')
    issued_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"Certificate for {self.recipient_name}"

    def get_verify_url(self):
        return f"/verify/{self.id}/"


class VerificationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
        related_name='verification_logs'
    )
    verified_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ['-verified_at']

    def __str__(self):
        return f"Verified {self.certificate} at {self.verified_at}"
