from django.contrib import admin
from certificates.models import CertificateTemplate, Certificate, VerificationLog


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'category', 'certificate_count', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'organization__name']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['recipient_name', 'organization', 'status', 'cert_hash', 'issued_at']
    list_filter = ['status', 'issued_at']
    search_fields = ['recipient_name', 'recipient_email']
    readonly_fields = ['id', 'issued_at']


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ['certificate', 'verified_at', 'ip_address', 'is_valid']
    list_filter = ['is_valid', 'verified_at']
