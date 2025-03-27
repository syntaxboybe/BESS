from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(DocumentStatus)
admin.site.register(clearance)
admin.site.register(CertificateOfIndigency)
admin.site.register(BuildingPermit)
admin.site.register(BusinessPermit)
admin.site.register(ResidencyCertificate)
admin.site.register(Notification)
admin.site.register(SupportingDocument)
admin.site.register(IndigencyDocument)
admin.site.register(BusinessDocument)
admin.site.register(BuildingDocument)
admin.site.register(ResidencyDocument)
