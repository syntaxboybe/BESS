from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from apps.UserPortal.models import BuildingPermit, BuildingDocument
from .forms import *
from project.utils import render_to_pdf
from .decorators import admin_only
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def building_permit_module(request):
    if request.user.is_authenticated:
        return render(request, "BuildingPermit/building_permit_module.html")
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def building_permit_list(request):
    if request.user.is_authenticated:
        context = {
            "building_permit_list": BuildingPermit.objects.all().order_by("-id")}
        return render(request, "BuildingPermit/building_permit_list.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_building_permit(request, id):
    if request.user.is_authenticated:
        building_permit = BuildingPermit.objects.get(pk=id)
        form = BuildingPermitForm(instance=building_permit)

        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been on process"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been received and is currently forwarded to kapitan. We will notify you once your request has been approved and is ready for pick-up. If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if building_permit.status.document_status == "Pending":
                new_status = DocumentStatus.objects.get(
                    document_status="Forwarded to Kapitan"
                )
                building_permit.status = new_status
                building_permit.save()

            form = BuildingPermitForm(request.POST, request.FILES, instance=building_permit)
            if form.is_valid():
                form.save()

                # Process any new file uploads
                files = request.FILES.getlist('documents[]')
                for file in files:
                    BuildingDocument.objects.create(
                        building_permit=building_permit,
                        document=file
                    )

            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"form": form, "disabledform": building_permit}
        return render(request, "BuildingPermit/building_permit_form.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def generate_building_permit(request, id):
    if request.user.is_authenticated:
        template_name = "BuildingPermit/building_permit_pdf.html"
        building_permit = BuildingPermit.objects.get(pk=id)

        return render_to_pdf(
            template_name,
            {
                "building_permit": building_permit,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def unsign_building_permit(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)
        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request are ready to claim"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been approved and is ready for pick-up. Kindy prepare the necessary documents for claiming.
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if building_permit.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim"
                )
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/unsign_building_permit.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def confirm_button_bldp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)

        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been officially released"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been officially released. Thank you for your using our service!
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            if building_permit.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/confirm_button_bldp.html", context)
    else:
        return redirect("loginPage")


def delete_building_permit(request, id):
    if request.user.is_authenticated:
        try:
            building_permit = BuildingPermit.objects.get(pk=id)
        except BuildingPermit.DoesNotExist:
            return HttpResponse("Building Permit not found.", status=404)

        username = building_permit.res_id.user.username
        context = {"building_permit": building_permit}

        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Reasons For Denying your Request"
            message = f"""
            Dear {username},

            Thank you for reaching out and submitting your request. After careful consideration, we regret to inform you that we are unable to accommodate your request at this time due to the following reason:

            {email_msg}

            We appreciate your understanding and the effort you put into presenting your request. If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            If there is an opportunity to revisit this in the future, we would be glad to reconnect. In the meantime, please feel free to reach out if there are other matters we can assist with.

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            # Update status to "Reverted"
            try:
                new_status = DocumentStatus.objects.get(
                    document_status="Reverted")
                building_permit.status = (
                    new_status  # Assign the DocumentStatus instance
                )
                building_permit.save()
            except DocumentStatus.DoesNotExist:
                return HttpResponse("DocumentStatus 'Reverted' not found.", status=500)

            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        return render(request, "BuildingPermit/delete_building_permit.html", context)

    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def no_sign_buildingpermit(request, id):
    if request.user.is_authenticated:
        template_name = "BuildingPermit/no_sign_buildingpermit_pdf.html"
        building_permit = BuildingPermit.objects.get(pk=id)

        return render_to_pdf(
            template_name,
            {
                "building_permit": building_permit,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_building_permit(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)
        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request are ready to claim"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been approved and is ready for pick-up. Kindy prepare the necessary documents for claiming.
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if building_permit.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim(e-Signed)"
                )
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/esign_building_permit.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_button_bldp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)
        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been officially released"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been officially released. Thank you for your using our service!
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if building_permit.status.document_status == "Ready to Claim(e-Signed)":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/esign_button_bldp.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_unsign_bldp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)

        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been officially released"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been officially released. Thank you for your using our service!
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            if building_permit.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/release_unsign_bldp.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_esigned_bldp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        building_permit = get_object_or_404(BuildingPermit, pk=id)
        form = BuildingPermitForm(instance=building_permit)
        username = building_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been officially released"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been officially released. Thank you for your using our service!
            If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {building_permit.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={building_permit.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [building_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if building_permit.status.document_status == "Ready to Claim(e-Signed)":
                new_status = DocumentStatus.objects.get(
                    document_status="Released(e-Signed)"
                )
                building_permit.status = new_status
                building_permit.save()
                form = BuildingPermitForm(
                    request.POST, instance=building_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BuildingPermitList"}
            )

        context = {"BuildingPermit": building_permit}
        return render(request, "BuildingPermit/release_esigned_bldp.html", context)
    else:
        return redirect("loginPage")
