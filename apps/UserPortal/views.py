from atexit import register
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from .decorators import user_superAdmin
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from apps.AnnouncementManagement.models import Announcement
from .forms import *
from .models import clearance as clr,CertificateOfIndigency as coi,BuildingPermit as buildingpermit, BusinessPermit as businesspermit, ResidencyCertificate as rescert, SupportingDocument, IndigencyDocument, BusinessDocument, BuildingDocument, ResidencyDocument
from .notification_utils import count_pending_requests, mark_as_read, create_notification





# Create your views here.

def home(request):
    return render(request, "UsersideTemplate/index.html")


def about(request):
     return render(request, "UsersideTemplate/about.html")

def contact(request):
    return render(request, "UsersideTemplate/contact.html")

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
@user_superAdmin
def servicesPortal(request):
    if request.user.is_authenticated:
        return render(request, "UsersideTemplate/service_portal.html")
    else:
        return redirect('loginPage')


def userLogout(request):
     logout(request)
     messages.success(request, 'logout successfully')
     return redirect(reverse('loginPage'))


def about(request):
    return render(request, "UsersideTemplate/about.html")

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def barangay_clearance(request):
    if request.user.is_authenticated:
        form = CleranceForm
        userid = request.user.residentsinfo
        if request.method == 'POST':
            form = CleranceForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    docs = clr.objects.filter(res_id=userid)
                    if docs.get(status=1):
                        messages.error(request, 'You still have pending request in Barangay Clearance')
                        return redirect('service_portal')
                except clr.DoesNotExist:
                    # Save the clearance form first
                    instance = form.save(commit=False)
                    instance.res_id = userid
                    instance.save()

                    # Process multiple document uploads
                    files = request.FILES.getlist('documents[]')
                    for file in files:
                        SupportingDocument.objects.create(
                            clearance=instance,
                            document=file
                        )

                    # Create notification for the new clearance request
                    create_notification('clearance', instance)

                    messages.success(request, 'Your request has been submitted. You can see your request status at Document Status')
                    return redirect('service_portal')

        context={'form':form}
        return render(request, 'UsersideTemplate/barangay_clearance.html', context)
    else:
        return redirect('loginPage')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def indigency(request):
    if request.user.is_authenticated:
        form = IndigencyForm
        userid = request.user.residentsinfo
        if request.method == 'POST':
            form = IndigencyForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    docs = coi.objects.filter(res_id=userid)
                    if docs.get(status=1):
                        messages.error(request, 'You still have pending request in Certificate of Indigency')
                        return redirect('service_portal')
                except coi.DoesNotExist:
                    # Save the indigency form first
                    instance = form.save(commit=False)
                    instance.res_id = userid
                    instance.save()

                    # Process multiple document uploads
                    files = request.FILES.getlist('documents[]')
                    for file in files:
                        IndigencyDocument.objects.create(
                            indigency=instance,
                            document=file
                        )

                    # Create notification for the new indigency request
                    create_notification('indigency', instance)

                    messages.success(request, 'Your request has been submitted. You can see your request status at Document Status')
                    return redirect('service_portal')
        context={'form':form}
        return render(request, "UsersideTemplate/indigency.html", context)
    else:
        return redirect('loginPage')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def BuildingPermit(request):
    if request.user.is_authenticated:
        form = BuildingPermitForm
        userid = request.user.residentsinfo
        if request.method == 'POST':
            form = BuildingPermitForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    docs = buildingpermit.objects.filter(res_id=userid)
                    if docs.get(status=1):
                        messages.error(request, 'You still have pending request in Building Permit')
                        return redirect('service_portal')
                except buildingpermit.DoesNotExist:
                    # Save the building permit form first
                    instance = form.save(commit=False)
                    instance.res_id = userid
                    instance.save()

                    # Process multiple document uploads
                    files = request.FILES.getlist('documents[]')
                    for file in files:
                        BuildingDocument.objects.create(
                            building_permit=instance,
                            document=file
                        )

                    # Create notification for the new building permit request
                    create_notification('building', instance)

                    messages.success(request, 'Your request has been submitted. You can see your request status at Document Status')
                    return redirect('service_portal')

        context={'form':form}
        return render(request, "UsersideTemplate/building_permit.html", context)
    else:
        return redirect('loginPage')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def BusinessPermit(request):
    if request.user.is_authenticated:
        form = BusinessPermitForm
        userid = request.user.residentsinfo
        if request.method == 'POST':
            form = BusinessPermitForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    docs = businesspermit.objects.filter(res_id=userid)
                    if docs.get(status=1):
                        messages.error(request, 'You still have pending request in Business Permit')
                        return redirect('service_portal')
                except businesspermit.DoesNotExist:
                    # Save the business permit form first
                    instance = form.save(commit=False)
                    instance.res_id = userid
                    instance.save()

                    # Process multiple document uploads
                    files = request.FILES.getlist('documents[]')
                    for file in files:
                        BusinessDocument.objects.create(
                            business_permit=instance,
                            document=file
                        )

                    # Create notification for the new business permit request
                    create_notification('business', instance)

                    messages.success(request, 'Your request has been submitted. You can see your request status at Document Status')
                    return redirect('service_portal')
        context={'form':form}
        return render(request, "UsersideTemplate/business_permit.html", context)
    else:
        return redirect('loginPage')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def ResidencyCertificate(request):
    if request.user.is_authenticated:
        form = ResidencyCertificateForm
        userid = request.user.residentsinfo
        userinfo = request.user
        if request.method == 'POST':
            form = ResidencyCertificateForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    docs = rescert.objects.filter(res_id=userid)
                    if docs.get(status=1):
                        messages.error(request, 'You still have pending request in Resident Certificate')
                        return redirect('service_portal')
                except rescert.DoesNotExist:
                    # Save the residency certificate form first
                    instance = form.save(commit=False)
                    instance.res_id = userid
                    instance.save()

                    # Process multiple document uploads
                    files = request.FILES.getlist('documents[]')
                    for file in files:
                        ResidencyDocument.objects.create(
                            residency_certificate=instance,
                            document=file
                        )

                    # Create notification for the new residency certificate request
                    create_notification('residency', instance)

                    messages.success(request, 'Your request has been submitted. You can see your request status at Document Status')
                    return redirect('service_portal')
        context={'form':form, 'userinfo':userinfo}
        return render(request, 'UsersideTemplate/residency_certificate.html', context)
    else:
        return redirect('loginPage')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'UsersideTemplate/profile.html')
    else:
        return redirect('loginPage')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def changeEmail(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateEmailForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your email has been updated')
                return redirect('profile')
            else:
                for key, error in list(form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, "You must pass the reCAPTCHA test")
                        continue

                    messages.error(request, error)

        form = UpdateEmailForm(instance=request.user)
        context = {'form': form}
        return render(request, 'UsersideTemplate/change_email.html', context)
    else:
        return redirect('loginPage')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def changeUsername(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUsernameForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your username has been updated')
                return redirect('profile')
            else:
                for key, error in list(form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, "You must pass the reCAPTCHA test")
                        continue

                    messages.error(request, error)

        form = UpdateUsernameForm(instance=request.user)
        context = {'form': form}
        return render(request, 'UsersideTemplate/change_username.html', context)
    else:
        return redirect('loginPage')


def announce(request):
    # Get current time
    now = timezone.now()
    # Get all announcements ordered by post date
    announce_list = Announcement.objects.all().order_by('-post_date')

    # Add is_new flag for announcements less than 24 hours old
    for announcement in announce_list:
        time_diff = now - announcement.post_date
        announcement.is_new = time_diff.total_seconds() < 24 * 3600  # 24 hours in seconds

    context = {'announcementList': announce_list}
    return render(request, 'UsersideTemplate/announcement.html', context)



def document_status(request):


    user_id = request.user.residentsinfo.id
    clearance_status = clr.objects.filter(res_id=user_id)
    indigency_status = coi.objects.filter(res_id=user_id)
    business_status =   businesspermit.objects.filter(res_id=user_id)
    building_status = buildingpermit.objects.filter(res_id=user_id)
    residency_status = rescert.objects.filter(res_id=user_id)
    context = {
        'clearance_list': clearance_status,
        'indigency_list': indigency_status,
        'business_list' : business_status,
        'building_list' : building_status,
        'residency_list': residency_status
    }
    return render(request, 'UsersideTemplate/doc_status.html', context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="loginPage")
def privacy(request):
    if request.user.is_authenticated:
        return render(request, 'UsersideTemplate/privacy.html')
    else:
        return redirect('loginPage')

@login_required(login_url="loginPage")
def notification_count_api(request):
    """API endpoint to get notification counts and detailed request information"""
    # Only allow non-superadmin users to access this endpoint
    if hasattr(request.user, 'groups') and request.user.groups.exists():
        if request.user.groups.all()[0].name == 'superadmin' or request.user.id == 1:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Get basic counts
    counts = count_pending_requests()

    # Get latest requests with detailed information
    pending_status = DocumentStatus.objects.get(id=1)

    # Format clearance requests
    clearance_requests = []
    for req in clr.objects.filter(status=pending_status).order_by('-date_requested')[:5]:
        clearance_requests.append({
            'id': req.id,
            'resident_name': f"{req.res_id.firstname} {req.res_id.lastname}",
            'date_requested': req.date_requested.strftime("%b %d, %Y %I:%M %p"),
            'purpose': req.purpose
        })

    # Format indigency requests
    indigency_requests = []
    for req in coi.objects.filter(status=pending_status).order_by('-date_requested')[:5]:
        indigency_requests.append({
            'id': req.id,
            'resident_name': f"{req.res_id.firstname} {req.res_id.lastname}",
            'date_requested': req.date_requested.strftime("%b %d, %Y %I:%M %p"),
            'purpose': req.purpose
        })

    # Format business permit requests
    business_requests = []
    for req in businesspermit.objects.filter(status=pending_status).order_by('-date_requested')[:5]:
        business_requests.append({
            'id': req.id,
            'resident_name': f"{req.res_id.firstname} {req.res_id.lastname}",
            'date_requested': req.date_requested.strftime("%b %d, %Y %I:%M %p"),
            'business_name': req.business_name
        })

    # Format building permit requests
    building_requests = []
    for req in buildingpermit.objects.filter(status=pending_status).order_by('-date_requested')[:5]:
        building_requests.append({
            'id': req.id,
            'resident_name': f"{req.res_id.firstname} {req.res_id.lastname}",
            'date_requested': req.date_requested.strftime("%b %d, %Y %I:%M %p"),
            'location': req.location
        })

    # Format residency certificate requests
    residency_requests = []
    for req in rescert.objects.filter(status=pending_status).order_by('-date_requested')[:5]:
        residency_requests.append({
            'id': req.id,
            'resident_name': f"{req.res_id.firstname} {req.res_id.lastname}",
            'date_requested': req.date_requested.strftime("%b %d, %Y %I:%M %p"),
            'purpose': req.purpose
        })

    # Combine counts with detailed requests
    response_data = counts
    response_data.update({
        'clearanceRequests': clearance_requests,
        'indigencyRequests': indigency_requests,
        'businessRequests': business_requests,
        'buildingRequests': building_requests,
        'residencyRequests': residency_requests
    })

    return JsonResponse(response_data)

@login_required(login_url="loginPage")
@require_POST
def mark_notification_read(request, notification_id):
    """API endpoint to mark a notification as read"""
    # Only allow non-superadmin users to access this endpoint
    if hasattr(request.user, 'groups') and request.user.groups.exists():
        if request.user.groups.all()[0].name == 'superadmin' or request.user.id == 1:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

    success = mark_as_read(notification_id)
    if success:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Notification not found'}, status=404)

@login_required(login_url="loginPage")
@require_POST
def mark_all_notifications_read(request):
    """API endpoint to mark all notifications as read"""
    # Only allow non-superadmin users to access this endpoint
    if hasattr(request.user, 'groups') and request.user.groups.exists():
        if request.user.groups.all()[0].name == 'superadmin' or request.user.id == 1:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Mark all notifications as read
    from .models import Notification
    Notification.objects.filter(is_read=False).update(is_read=True)

    return JsonResponse({'status': 'success', 'message': 'All notifications marked as read'})
