from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from apps.UserPortal.models import BusinessPermit
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
def business_permit_module(request):
    if request.user.is_authenticated:
        return render(request, "BusinessPermit/business_permit_module.html")
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def business_permit_list(request):
    if request.user.is_authenticated:
        context = {
            "business_permit_list": BusinessPermit.objects.all().order_by("-id")}
        return render(request, "BusinessPermit/business_permit_list.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_business_permit(request, id):
    if request.user.is_authenticated:
        business_permit = BusinessPermit.objects.get(pk=id)
        form = BusinessPermitForm(instance=business_permit)

        business_permit_id = BusinessPermit.objects.get(pk=id)
        username = business_permit.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been on process"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been received and is currently forwarded to kapitan. We will notify you once your request has been approved and is ready for pick-up. If you have any questions or concerns, please do not hesitate to contact us at the following numbers:            
            Globe: 09361174734
            TM: 09057198345
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if business_permit.status.document_status == "Pending":
                new_status = DocumentStatus.objects.get(
                    document_status="Forwarded to Kapitan"
                )
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"form": form, "disabledform": business_permit_id}
        return render(request, "BusinessPermit/business_permit_form.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def generate_business_permit(request, id):
    if request.user.is_authenticated:
        template_name = "BusinessPermit/business_permit_pdf.html"
        business_permit = BusinessPermit.objects.get(pk=id)

        return render_to_pdf(
            template_name,
            {
                "business_permit": business_permit,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def unsign_business_permit(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if business_permit.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim"
                )
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/unsign_business_permit.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def confirm_button_bsp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if business_permit.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/confirm_button_bsp.html", context)
    else:
        return redirect("loginPage")


def delete_business_permit(request, id):
    if request.user.is_authenticated:
        try:
            business_permit = BusinessPermit.objects.get(pk=id)
        except BusinessPermit.DoesNotExist:
            return HttpResponse("Business Permit not found.", status=404)

        username = business_permit.res_id.user.username
        context = {"business_permit": business_permit}

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

            If there is an opportunity to revisit this in the future, we would be glad to reconnect. In the meantime, please feel free to reach out if there are other matters we can assist with.

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            # Update status to "Reverted"
            try:
                new_status = DocumentStatus.objects.get(
                    document_status="Reverted")
                business_permit.status = (
                    new_status  # Assign the DocumentStatus instance
                )
                business_permit.save()
            except DocumentStatus.DoesNotExist:
                return HttpResponse("DocumentStatus 'Reverted' not found.", status=500)

            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        return render(request, "BusinessPermit/delete_business_permit.html", context)

    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def no_sign_businesspermit(request, id):
    if request.user.is_authenticated:
        template_name = "BusinessPermit/no_sign_businesspermit_pdf.html"
        business_permit = BusinessPermit.objects.get(pk=id)

        return render_to_pdf(
            template_name,
            {
                "business_permit": business_permit,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_business_permit(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if business_permit.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim(e-Signed)"
                )
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/esign_business_permit.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_button_bsp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            if business_permit.status.document_status == "Ready to Claim(e-Signed)":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/esign_button_bsp.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_unsign_bsp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            if business_permit.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/release_unsign_bsp.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_esigned_bsp(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        business_permit = get_object_or_404(BusinessPermit, pk=id)
        form = BusinessPermitForm(instance=business_permit)

        username = business_permit.res_id.user.username
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
            
            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [business_permit.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            if business_permit.status.document_status == "Ready to Claim(e-Signed)":
                new_status = DocumentStatus.objects.get(
                    document_status="Released(e-Signed)"
                )
                business_permit.status = new_status
                business_permit.save()
            form = BusinessPermitForm(request.POST, instance=business_permit)
            if form.is_valid():
                form.save()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "BusinessPermitlistUpdate"}
            )

        context = {"BusinessPermit": business_permit}
        return render(request, "BusinessPermit/release_esigned_bsp.html", context)
    else:
        return redirect("loginPage")
