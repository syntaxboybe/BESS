from django.shortcuts import render, redirect
from apps.ResidentManagement.models import ResidentsInfo
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .decorators import admin_only
from django.contrib.auth.models import User as user
# Import document models
from apps.UserPortal.models import clearance, CertificateOfIndigency, BusinessPermit, BuildingPermit, ResidencyCertificate, DocumentStatus
# Add imports for date filtering and JSON response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from datetime import datetime, timedelta
from django.utils import timezone
import calendar
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
@ensure_csrf_cookie
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

        # Get Released status (document_status="Released" or "Released(e-Signed)")
        released_statuses = DocumentStatus.objects.filter(document_status__in=["Released", "Released(e-Signed)"])

        # Get Reverted status (document_status="Reverted")
        reverted_status = DocumentStatus.objects.filter(document_status="Reverted").first()

        # Clearance statistics
        clearance_total = clearance.objects.all().count()
        clearance_pending = clearance.objects.filter(status=pending_status).count()
        clearance_released = clearance.objects.filter(status__in=released_statuses).count()
        clearance_reverted = clearance.objects.filter(status=reverted_status).count() if reverted_status else 0

        # Indigency statistics
        indigency_total = CertificateOfIndigency.objects.all().count()
        indigency_pending = CertificateOfIndigency.objects.filter(status=pending_status).count()
        indigency_released = CertificateOfIndigency.objects.filter(status__in=released_statuses).count()
        indigency_reverted = CertificateOfIndigency.objects.filter(status=reverted_status).count() if reverted_status else 0

        # Business permit statistics
        business_total = BusinessPermit.objects.all().count()
        business_pending = BusinessPermit.objects.filter(status=pending_status).count()
        business_released = BusinessPermit.objects.filter(status__in=released_statuses).count()
        business_reverted = BusinessPermit.objects.filter(status=reverted_status).count() if reverted_status else 0

        # Building permit statistics
        building_total = BuildingPermit.objects.all().count()
        building_pending = BuildingPermit.objects.filter(status=pending_status).count()
        building_released = BuildingPermit.objects.filter(status__in=released_statuses).count()
        building_reverted = BuildingPermit.objects.filter(status=reverted_status).count() if reverted_status else 0

        # Residency certificate statistics
        residency_total = ResidencyCertificate.objects.all().count()
        residency_pending = ResidencyCertificate.objects.filter(status=pending_status).count()
        residency_released = ResidencyCertificate.objects.filter(status__in=released_statuses).count()
        residency_reverted = ResidencyCertificate.objects.filter(status=reverted_status).count() if reverted_status else 0

        # Calculate totals across all documents
        document_total = clearance_total + indigency_total + business_total + building_total + residency_total
        pending_total = clearance_pending + indigency_pending + business_pending + building_pending + residency_pending
        released_total = clearance_released + indigency_released + business_released + building_released + residency_released
        reverted_total = clearance_reverted + indigency_reverted + business_reverted + building_reverted + residency_reverted

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
            "clearance_released": clearance_released,
            "clearance_reverted": clearance_reverted,

            "indigency_total": indigency_total,
            "indigency_pending": indigency_pending,
            "indigency_released": indigency_released,
            "indigency_reverted": indigency_reverted,

            "business_total": business_total,
            "business_pending": business_pending,
            "business_released": business_released,
            "business_reverted": business_reverted,

            "building_total": building_total,
            "building_pending": building_pending,
            "building_released": building_released,
            "building_reverted": building_reverted,

            "residency_total": residency_total,
            "residency_pending": residency_pending,
            "residency_released": residency_released,
            "residency_reverted": residency_reverted,

            "document_total": document_total,
            "pending_total": pending_total,
            "released_total": released_total,
            "reverted_total": reverted_total,
        }

        return render(request, "Dashboard/demographic.html", context)

    else:
        return redirect("loginPage")

@csrf_exempt
@login_required(login_url="loginPage")
@admin_only
def filter_stats(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            period = data.get('period', 'all')
            week = data.get('week', 'current')
            month = int(data.get('month', datetime.now().month))
            year = int(data.get('year', datetime.now().year))

            # Get document statuses
            pending_status = DocumentStatus.objects.get(id=1)
            released_statuses = DocumentStatus.objects.filter(document_status__in=["Released", "Released(e-Signed)"])
            reverted_status = DocumentStatus.objects.filter(document_status="Reverted").first()

            # Calculate date range for filtering
            start_date = None
            end_date = timezone.now()

            if period == 'weekly':
                # Calculate start of week
                today = timezone.now().date()
                # Find the start of the week (Monday)
                start_of_current_week = today - timedelta(days=today.weekday())

                if week == 'current':
                    start_date = timezone.make_aware(datetime.combine(start_of_current_week, datetime.min.time()))
                elif week == 'last':
                    start_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=7), datetime.min.time()))
                    end_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(seconds=1), datetime.min.time()))
                elif week == 'last2':
                    start_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=14), datetime.min.time()))
                    end_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=7, seconds=1), datetime.min.time()))
                elif week == 'last3':
                    start_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=21), datetime.min.time()))
                    end_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=14, seconds=1), datetime.min.time()))
                elif week == 'last4':
                    start_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=28), datetime.min.time()))
                    end_date = timezone.make_aware(datetime.combine(start_of_current_week - timedelta(days=21, seconds=1), datetime.min.time()))

            elif period == 'monthly':
                # First day of the selected month
                _, last_day = calendar.monthrange(year, month)
                start_date = timezone.make_aware(datetime(year, month, 1, 0, 0, 0))

                # Last day of the selected month
                if month == datetime.now().month and year == datetime.now().year:
                    end_date = timezone.now()
                else:
                    end_date = timezone.make_aware(datetime(year, month, last_day, 23, 59, 59))

            elif period == 'yearly':
                # First day of the selected year
                start_date = timezone.make_aware(datetime(year, 1, 1, 0, 0, 0))

                # Last day of the selected year
                if year == datetime.now().year:
                    end_date = timezone.now()
                else:
                    end_date = timezone.make_aware(datetime(year, 12, 31, 23, 59, 59))

            # Query filtering function
            def filter_by_date(queryset):
                if start_date:
                    return queryset.filter(date_requested__gte=start_date, date_requested__lte=end_date)
                return queryset  # Return all data for 'all' period

            # Filter document statistics
            # Clearance statistics
            clearance_queryset = filter_by_date(clearance.objects.all())
            clearance_total = clearance_queryset.count()
            clearance_pending = clearance_queryset.filter(status=pending_status).count()
            clearance_released = clearance_queryset.filter(status__in=released_statuses).count()
            clearance_reverted = clearance_queryset.filter(status=reverted_status).count() if reverted_status else 0

            # Indigency statistics
            indigency_queryset = filter_by_date(CertificateOfIndigency.objects.all())
            indigency_total = indigency_queryset.count()
            indigency_pending = indigency_queryset.filter(status=pending_status).count()
            indigency_released = indigency_queryset.filter(status__in=released_statuses).count()
            indigency_reverted = indigency_queryset.filter(status=reverted_status).count() if reverted_status else 0

            # Business permit statistics
            business_queryset = filter_by_date(BusinessPermit.objects.all())
            business_total = business_queryset.count()
            business_pending = business_queryset.filter(status=pending_status).count()
            business_released = business_queryset.filter(status__in=released_statuses).count()
            business_reverted = business_queryset.filter(status=reverted_status).count() if reverted_status else 0

            # Building permit statistics
            building_queryset = filter_by_date(BuildingPermit.objects.all())
            building_total = building_queryset.count()
            building_pending = building_queryset.filter(status=pending_status).count()
            building_released = building_queryset.filter(status__in=released_statuses).count()
            building_reverted = building_queryset.filter(status=reverted_status).count() if reverted_status else 0

            # Residency certificate statistics
            residency_queryset = filter_by_date(ResidencyCertificate.objects.all())
            residency_total = residency_queryset.count()
            residency_pending = residency_queryset.filter(status=pending_status).count()
            residency_released = residency_queryset.filter(status__in=released_statuses).count()
            residency_reverted = residency_queryset.filter(status=reverted_status).count() if reverted_status else 0

            # Calculate totals across all documents
            document_total = clearance_total + indigency_total + business_total + building_total + residency_total
            pending_total = clearance_pending + indigency_pending + business_pending + building_pending + residency_pending
            released_total = clearance_released + indigency_released + business_released + building_released + residency_released
            reverted_total = clearance_reverted + indigency_reverted + business_reverted + building_reverted + residency_reverted

            # Prepare response
            response_data = {
                'clearance': {
                    'total': clearance_total,
                    'pending': clearance_pending,
                    'released': clearance_released,
                    'reverted': clearance_reverted
                },
                'indigency': {
                    'total': indigency_total,
                    'pending': indigency_pending,
                    'released': indigency_released,
                    'reverted': indigency_reverted
                },
                'business': {
                    'total': business_total,
                    'pending': business_pending,
                    'released': business_released,
                    'reverted': business_reverted
                },
                'building': {
                    'total': building_total,
                    'pending': building_pending,
                    'released': building_released,
                    'reverted': building_reverted
                },
                'residency': {
                    'total': residency_total,
                    'pending': residency_pending,
                    'released': residency_released,
                    'reverted': residency_reverted
                },
                'all': {
                    'total': document_total,
                    'pending': pending_total,
                    'released': released_total,
                    'reverted': reverted_total
                }
            }

            return JsonResponse(response_data)

        except Exception as e:
            import traceback
            print(f"Error in filter_stats: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
