from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from apps.UserPortal.models import clearance as clerance_list
from .forms import *
from project.utils import render_to_pdf
from .decorators import admin_only
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def clearance(request):
    if request.user.is_authenticated:
        return render(request, "ClearanceManagement/clearance_table.html")
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def clearance_list(request):
    if request.user.is_authenticated:
        context = {"clearance_list": clerance_list.objects.all().order_by("id")}
        return render(request, "ClearanceManagement/clearance_list.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_clearance(request, id):
    if request.user.is_authenticated:

        clearance = clerance_list.objects.get(pk=id)
        form = cleranceForm(instance=clearance)

        if request.method == "POST":
            form = cleranceForm(
                request.POST, request.FILES, instance=clearance
            )  # Include request.FILES
            if form.is_valid():
                form.save()
                return HttpResponse(
                    status=204, headers={"HX-Trigger": "clearancelistUpdate"}
                )

        context = {"form": form, "disabledform": clearance}
        return render(request, "ClearanceManagement/clearance_form.html", context)
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
def generate_clearance(request, id):
    if request.user.is_authenticated:
        template_name = "ClearanceManagement/clearance_pdf.html"
        clearance = get_object_or_404(clerance_list, pk=id)
        birthdate = clearance.res_id.birthdate
        age = calculate_age(birthdate)
        # Fetch clearance object and related data
        # Ensure the media URL is passed to handle images
        context = {
            "clearance": clearance,
            "media_url": request.build_absolute_uri(settings.MEDIA_URL),
            "age": age,
        }

        return render_to_pdf(template_name, context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def esign_clearance(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        clearance = get_object_or_404(clerance_list, pk=id)

        if request.method == "POST":
            # Logic to mark clearance as signed
            clearance.is_signed = True  # Assuming there's an `is_signed` field
            clearance.save()

            # Optionally process a confirmation message
            confirmation_message = request.POST.get("confirmation_message", "")

            # Send a response for htmx or redirect
            return HttpResponse(
                status=204, headers={"HX-Trigger": "clearancelistUpdate"}
            )
            return redirect("clearance_list")

        context = {"clearance": clearance}
        return render(request, "ClearanceManagement/esign_clearance.html", context)
    else:
        return redirect("loginPage")


def delete_clearance(request, id):
    if request.user.is_authenticated:
        clearance = clerance_list.objects.get(pk=id)
        username = clearance.res_id.user.username
        context = {"clearance": clearance}
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
            recipient_list = [clearance.res_id.user.email]
            send_mail(subject, message, email_from, recipient_list)

            clearance.delete()
            return HttpResponse(
                status=204, headers={"HX-Trigger": "clearancelistUpdate"}
            )
        return render(request, "ClearanceManagement/delete_clearance.html", context)

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
def no_sign_clearance(request, id):
    if request.user.is_authenticated:
        template_name = "ClearanceManagement/no_sign_pdf.html"
        clearance = get_object_or_404(clerance_list, pk=id)
        birthdate = clearance.res_id.birthdate
        age = calculate_age(birthdate)
        # Fetch clearance object and related data
        # Ensure the media URL is passed to handle images
        context = {
            "clearance": clearance,
            "media_url": request.build_absolute_uri(settings.MEDIA_URL),
            "age": age,
        }

        return render_to_pdf(template_name, context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def unsign_clearance(request, id):
    """
    Mark a clearance as signed.
    """
    if request.user.is_authenticated:
        clearance = get_object_or_404(clerance_list, pk=id)

        if request.method == "POST":
            # Logic to mark clearance as signed
            clearance.is_signed = True  # Assuming there's an `is_signed` field
            clearance.save()

            # Optionally process a confirmation message
            confirmation_message = request.POST.get("confirmation_message", "")

            # Send a response for htmx or redirect
            return HttpResponse(
                status=204, headers={"HX-Trigger": "clearancelistUpdate"}
            )
            return redirect("clearance_list")

        context = {"clearance": clearance}
        return render(request, "ClearanceManagement/unsign_clearance.html", context)
    else:
        return redirect("loginPage")
