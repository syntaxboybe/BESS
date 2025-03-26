from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from apps.UserPortal.models import ResidencyCertificate
from .forms import *
from project.utils import render_to_pdf
from .decorators import admin_only
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from datetime import date

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def residency_certificate_module(request):
    if request.user.is_authenticated:
        return render(request, "ResidencyCertificate/resident_certificate_module.html")
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def residency_certificate_list(request):
    if request.user.is_authenticated:
        context = {
            "residency_certificate_list": ResidencyCertificate.objects.all().order_by(
                "-id"
            )
        }
        return render(
            request, "ResidencyCertificate/residency_certificate_list.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_residency(request, id):
    if request.user.is_authenticated:
        residency_certificate = ResidencyCertificate.objects.get(pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)

        username = residency_certificate.res_id.user.username
        if request.method == "POST":
            email_msg = request.POST.get("reason_masage")

            # Prepare email content
            subject = "Good news! Your Request has been on process"
            message = f"""
            Dear {username},

            We are pleased to inform you that your request has been received and is currently forwarded to kapitan. We will notify you once your request has been approved and is ready for pick-up. If you have any questions or concerns, please do not hesitate to contact us at the following numbers:
            Globe: 09361174734
            TM: 09057198345

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if residency_certificate.status.document_status == "Pending":
                new_status = DocumentStatus.objects.get(
                    document_status="Forwarded to Kapitan"
                )
                residency_certificate.status = new_status
                residency_certificate.save()
                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        context = {"form": form, "disabledform": residency_certificate}
        return render(
            request, "ResidencyCertificate/residency_certificate_form.html", context
        )
    else:
        return redirect("loginPage")


def calculate_age(birthdate):
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def generate_resident_certificate(request, id):
    if request.user.is_authenticated:
        template_name = "ResidencyCertificate/resident_certificate_pdf.html"
        residency_certificate = ResidencyCertificate.objects.get(pk=id)
        birthdate = residency_certificate.res_id.birthdate
        age = calculate_age(birthdate)
        return render_to_pdf(
            template_name,
            {
                "residency_certificate": residency_certificate,
                "age": age,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def unsign_residency_cert(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)

        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if residency_certificate.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim"
                )
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/unsign_residency_cert.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def confirm_button_residency(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)
        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if residency_certificate.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/confirm_button_residency.html", context
        )
    else:
        return redirect("loginPage")


def delete_resident_certificate_request(request, id):
    if request.user.is_authenticated:
        try:
            residency_certificate = ResidencyCertificate.objects.get(pk=id)
        except ResidencyCertificate.DoesNotExist:
            return HttpResponse("Residency not found.", status=404)

        username = residency_certificate.res_id.user.username
        context = {"residency_certificate": residency_certificate}

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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            If there is an opportunity to revisit this in the future, we would be glad to reconnect. In the meantime, please feel free to reach out if there are other matters we can assist with.

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)

            # Update status to "Reverted"
            try:
                new_status = DocumentStatus.objects.get(
                    document_status="Reverted")
                residency_certificate.status = (
                    new_status  # Assign the DocumentStatus instance
                )
                residency_certificate.save()
            except DocumentStatus.DoesNotExist:
                return HttpResponse("DocumentStatus 'Reverted' not found.", status=500)

            return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        return render(
            request,
            "ResidencyCertificate/delete_resident_certificate.html",
            context,
        )

    else:
        return redirect("loginPage")


def calculate_age(birthdate):
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def no_sign_residencycert(request, id):
    if request.user.is_authenticated:
        template_name = "ResidencyCertificate/no_sign_residencycert_pdf.html"
        residency_certificate = ResidencyCertificate.objects.get(pk=id)
        birthdate = residency_certificate.res_id.birthdate
        age = calculate_age(birthdate)
        return render_to_pdf(
            template_name,
            {
                "residency_certificate": residency_certificate,
                "age": age,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_residency_cert(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)

        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if residency_certificate.status.document_status == "Forwarded to Kapitan":
                new_status = DocumentStatus.objects.get(
                    document_status="Ready to Claim(e-Signed)"
                )
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/esign_residency_cert.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_button_residency(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)
        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if (
                residency_certificate.status.document_status
                == "Ready to Claim(e-Signed)"
            ):
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        # Render the page if the request method is GET
        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/esign_button_residency.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_esigned_residency(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)
        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if (
                residency_certificate.status.document_status
                == "Ready to Claim(e-Signed)"
            ):
                new_status = DocumentStatus.objects.get(
                    document_status="Released(e-Signed)"
                )
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        # Render the page if the request method is GET
        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/release_esigned_residency.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def release_unsign_residency(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        residency_certificate = get_object_or_404(ResidencyCertificate, pk=id)
        form = ResidencyCertificateForm(instance=residency_certificate)
        username = residency_certificate.res_id.user.username
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

            Transaction ID: {residency_certificate.transaction_id}
            You can track your document status anytime at: {request.build_absolute_uri('/document_tracker/')}?txn={residency_certificate.transaction_id}

            Sincerely,
            The Barangay E-Service Team
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [residency_certificate.res_id.user.email]

            # Send email
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
            if residency_certificate.status.document_status == "Ready to Claim":
                new_status = DocumentStatus.objects.get(
                    document_status="Released")
                residency_certificate.status = new_status
                residency_certificate.is_signed = (
                    True  # Assuming there's an `is_signed` field
                )
                residency_certificate.save()

                form = ResidencyCertificateForm(
                    request.POST, instance=residency_certificate
                )
                if form.is_valid():
                    form.save()
                return HttpResponse(status=204, headers={"HX-Trigger": "ResidencyList"})

        context = {"ResidencyCert": residency_certificate}
        return render(
            request, "ResidencyCertificate/release_unsign_residency.html", context
        )
    else:
        return redirect("loginPage")
