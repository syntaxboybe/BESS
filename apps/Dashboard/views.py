from django.shortcuts import render, redirect
from apps.ResidentManagement.models import ResidentsInfo
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .decorators import admin_only
from django.contrib.auth.models import User as user
# Import document models
from apps.UserPortal.models import clearance, CertificateOfIndigency, BusinessPermit, BuildingPermit, ResidencyCertificate, DocumentStatus
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def dashboard(request):
    if request.user.is_authenticated:
        cMale = ResidentsInfo.objects.filter(sex_id="1").count
        cFemale = ResidentsInfo.objects.filter(sex_id="2").count

        cMarried = ResidentsInfo.objects.filter(civil_status="1").count
        cSingle = ResidentsInfo.objects.filter(civil_status="2").count
        cDivorced = ResidentsInfo.objects.filter(civil_status="3").count
        cWidowed = ResidentsInfo.objects.filter(civil_status="4").count

        cYes = ResidentsInfo.objects.filter(single_parent="Yes").count

        cPwd = ResidentsInfo.objects.filter(status="2").count
        cSenior = ResidentsInfo.objects.filter(status="3").count

        cResident = ResidentsInfo.objects.all().count

        # Get document statistics
        # Pending status (id=1)
        pending_status = DocumentStatus.objects.get(id=1)

        # Clearance statistics
        clearance_total = clearance.objects.all().count()
        clearance_pending = clearance.objects.filter(status=pending_status).count()

        # Indigency statistics
        indigency_total = CertificateOfIndigency.objects.all().count()
        indigency_pending = CertificateOfIndigency.objects.filter(status=pending_status).count()

        # Business permit statistics
        business_total = BusinessPermit.objects.all().count()
        business_pending = BusinessPermit.objects.filter(status=pending_status).count()

        # Building permit statistics
        building_total = BuildingPermit.objects.all().count()
        building_pending = BuildingPermit.objects.filter(status=pending_status).count()

        # Residency certificate statistics
        residency_total = ResidencyCertificate.objects.all().count()
        residency_pending = ResidencyCertificate.objects.filter(status=pending_status).count()

        # Calculate totals across all documents
        document_total = clearance_total + indigency_total + business_total + building_total + residency_total
        pending_total = clearance_pending + indigency_pending + business_pending + building_pending + residency_pending

        context = {
            "cResident": cResident,
            "cMale": cMale,
            "cFemale": cFemale,
            "cMarried": cMarried,
            "cSingle": cSingle,
            "cDivorced": cDivorced,
            "cWidowed": cWidowed,
            "cYes": cYes,
            "cPwd": cPwd,
            "cSenior": cSenior,
            "resident_list": user.objects.filter(
                groups__name__in=["resident"]
            ).order_by("id"),
            # Document statistics
            "clearance_total": clearance_total,
            "clearance_pending": clearance_pending,
            "indigency_total": indigency_total,
            "indigency_pending": indigency_pending,
            "business_total": business_total,
            "business_pending": business_pending,
            "building_total": building_total,
            "building_pending": building_pending,
            "residency_total": residency_total,
            "residency_pending": residency_pending,
            "document_total": document_total,
            "pending_total": pending_total,
        }

        return render(request, "Dashboard/demographic.html", context)

    else:
        return redirect("loginPage")
