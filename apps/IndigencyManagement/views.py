from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from apps.UserPortal.models import CertificateOfIndigency
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
def indigency_module(request):
    if request.user.is_authenticated:
        return render(request, "IndigencyManagement/indigency_module.html")
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def indigency_list(request):
    if request.user.is_authenticated:
        context = {
            "indigency_list": CertificateOfIndigency.objects.all().order_by("id")
        }
        return render(request, "IndigencyManagement/indigency_list.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_indigency(request, id):
    if request.user.is_authenticated:
        indigency = CertificateOfIndigency.objects.get(pk=id)
        form = indigencyForm(instance=indigency)

        indigency_id = CertificateOfIndigency.objects.get(pk=id)
        if request.method == "POST":
            form = indigencyForm(request.POST, instance=indigency)
            if form.is_valid():
                form.save()
                return HttpResponse(
                    status=204, headers={"HX-Trigger": "indigencylistUpdate"}
                )

        context = {"form": form, "disabledform": indigency_id}
        return render(request, "IndigencyManagement/indigency_form.html", context)
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
def generate_indigency(request, id):
    if request.user.is_authenticated:
        template_name = "IndigencyManagement/indigency_pdf.html"
        indigency = CertificateOfIndigency.objects.get(pk=id)
        birthdate = indigency.res_id.birthdate
        age = calculate_age(birthdate)
        return render_to_pdf(
            template_name,
            {
                "indigency": indigency,
                "age": age,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def unsign_indigency_cert(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        indigency_cert = get_object_or_404(CertificateOfIndigency, pk=id)

        if request.method == "POST":
            # Logic to mark clearance as signed
            indigency_cert.is_signed = True  # Assuming there's an `is_signed` field
            indigency_cert.save()

            # Optionally process a confirmation message
            confirmation_message = request.POST.get("confirmation_message", "")

            # Send a response for htmx or redirect
            return HttpResponse(
                status=204, headers={"HX-Trigger": "IndigencyCertUpdate"}
            )
            return redirect("IndigencyManagement")

        context = {"IndigencyCert": indigency_cert}
        return render(
            request, "IndigencyManagement/unsign_indigency_cert.html", context
        )
    else:
        return redirect("loginPage")


def delete_indigency(request, id):
    if request.user.is_authenticated:
        indigency = CertificateOfIndigency.objects.get(pk=id)
        username = indigency.res_id.user.username
        context = {"indigency": indigency}
        if request.method == "POST":

            email_msg = request.POST.get("reason_masage")

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
            recipient_list = [indigency.res_id.user.email]
            send_mail(subject, message, email_from, recipient_list)

            indigency.delete()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "indigencylistUpdate"}
            )
        return render(request, "IndigencyManagement/delete_indigency.html", context)

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
def no_sign_indigencycert(request, id):
    if request.user.is_authenticated:
        template_name = "IndigencyManagement/no_sign_indigencycert_pdf.html"
        indigency = CertificateOfIndigency.objects.get(pk=id)
        birthdate = indigency.res_id.birthdate
        age = calculate_age(birthdate)
        return render_to_pdf(
            template_name,
            {
                "indigency": indigency,
                "age": age,
            },
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_indigency_cert(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        indigency_cert = get_object_or_404(CertificateOfIndigency, pk=id)

        if request.method == "POST":
            # Logic to mark clearance as signed
            indigency_cert.is_signed = True  # Assuming there's an `is_signed` field
            indigency_cert.save()

            # Optionally process a confirmation message
            confirmation_message = request.POST.get("confirmation_message", "")

            # Send a response for htmx or redirect
            return HttpResponse(
                status=204, headers={"HX-Trigger": "IndigencyCertUpdate"}
            )
            return redirect("IndigencyManagement")

        context = {"IndigencyCert": indigency_cert}
        return render(request, "IndigencyManagement/esign_indigency_cert.html", context)
    else:
        return redirect("loginPage")
