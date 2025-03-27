from email.policy import default
from django.db import models

from apps.ResidentManagement.models import*
import uuid

# Create your models here.


class DocumentStatus(models.Model):
    document_status = models.CharField(max_length=70)

    def __str__(self):
        return self.document_status


class clearance(models.Model):
    document_type = models.CharField(max_length=70, default="Barangay Clearance")
    res_id = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE, null=True)
    age = models.CharField(max_length=70)
    purpose = models.CharField(max_length=70)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(null=True)

    community_tax_num = models.CharField(max_length=70, null=True)
    community_tax_date_issued = models.DateField(null=True)

    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class CertificateOfIndigency(models.Model):
    document_type = models.CharField(max_length=70, default="Certificate of Indigency")
    res_id = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE, null=True)
    age = models.CharField(max_length=70)
    purpose = models.CharField(max_length=70)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(null=True)
    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

class BuildingPermit(models.Model):
    document_type = models.CharField(max_length=70, default="Building Permit")
    res_id = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE, null=True)
    proposed_construction = models.CharField(max_length=255)
    total_area  = models.CharField(max_length=255)
    estimated_cost = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    contractor = models.CharField(max_length=255)
    prepared_by = models.CharField(max_length=255)

    paid_under_or = models.CharField(max_length=255)

    date_requested = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(null=True)

    amount_paid = models.CharField(max_length=255)

    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class BusinessPermit(models.Model):
    document_type = models.CharField(max_length=70, default="Business Permit")
    res_id = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE, null=True)
    business_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    business_nature = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    residece_certificate_no = models.CharField(max_length=255)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(null=True)
    issued_at = models.CharField(max_length=255)
    capital_investment = models.CharField(max_length=255)
    gross_sales = models.CharField(max_length=255)

    previous_or = models.CharField(max_length=255)
    date_issued = models.DateField(null=True)
    previous_or_issued_at = models.CharField(max_length=255)
    amount_collect = models.CharField(max_length=255)
    paid_or = models.CharField(max_length=255)
    paid_or_date_issued = models.DateField(null=True)
    paid_or_issued_at = models.CharField(max_length=255)
    amount_colledted = models.CharField(max_length=255)

    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class ResidencyCertificate (models.Model):
    document_type = models.CharField(max_length=70, default="Certificate of Residency")
    res_id = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE, null=True)
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(null=True)
    purpose = models.CharField(max_length=255)
    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1)


class Notification(models.Model):
    DOCUMENT_TYPES = (
        ('clearance', 'Barangay Clearance'),
        ('indigency', 'Certificate of Indigency'),
        ('business', 'Business Permit'),
        ('building', 'Building Permit'),
        ('residency', 'Certificate of Residency'),
    )

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    resident = models.ForeignKey(ResidentsInfo, on_delete=models.CASCADE)
    request_id = models.IntegerField()  # ID of the specific request
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.get_document_type_display()} request from {self.resident}"


class SupportingDocument(models.Model):
    clearance = models.ForeignKey(clearance, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='clearance_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.clearance.res_id} - {self.uploaded_at}"


class IndigencyDocument(models.Model):
    indigency = models.ForeignKey(CertificateOfIndigency, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='indigency_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.indigency.res_id} - {self.uploaded_at}"


class BusinessDocument(models.Model):
    business_permit = models.ForeignKey(BusinessPermit, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='business_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.business_permit.business_name} Business Permit"


class BuildingDocument(models.Model):
    building_permit = models.ForeignKey(BuildingPermit, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='building_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.building_permit.owner} Building Permit"


class ResidencyDocument(models.Model):
    residency_certificate = models.ForeignKey(ResidencyCertificate, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='residency_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.residency_certificate.res_id} Certificate of Residency"
