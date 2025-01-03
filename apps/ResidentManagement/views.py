from audioop import reverse
from tokenize import group
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from .forms import *
import face_recognition
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
from django.contrib.auth.models import User, Group
import os
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from .decorators import admin_only
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from apps.UserPortal.models import (
    clearance as clearance_list,
    CertificateOfIndigency,
    BusinessPermit,
    BuildingPermit,
    ResidencyCertificate,
    DocumentStatus,
)
from apps.ClearanceManagement.forms import *

from django.core.paginator import Paginator

from project.utils import render_to_pdf

from django.urls import reverse

import datetime

last_face = "no_face"
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, "sound/")
face_list_file = os.path.join(current_path, "face_list.txt")
sound = os.path.join(sound_folder, "beep.wav")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def resident_list(request):
    if request.user.is_authenticated:
        context = {
            "resident_list": User.objects.filter(
                groups__name__in=["resident"]
            ).order_by("last_name")
        }
        return render(request, "ResidentManagement/residents_list.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def pwd(request):
    if request.user.is_authenticated:
        context = {
            "pwd_list": User.objects.filter(residentsinfo__status=2).order_by(
                "last_name"
            )
        }
        return render(request, "ResidentManagement/pwd_resident.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def senior(request):
    if request.user.is_authenticated:
        context = {
            "senior_list": User.objects.filter(residentsinfo__status=3).order_by(
                "last_name"
            )
        }
        return render(request, "ResidentManagement/senior_resident.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def single(request):
    if request.user.is_authenticated:
        context = {
            "single_list": User.objects.filter(
                residentsinfo__single_parent="Yes"
            ).order_by("last_name")
        }
        return render(request, "ResidentManagement/single_list.html", context)
    else:
        return redirect("loginPage")


def adminLogout(request):
    logout(request)
    messages.success(request, "logout successfully")
    return redirect(reverse("loginPage"))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def ajax(request):
    if request.user.is_authenticated:
        last_face = LastFace.objects.last()
        context = {"last_face": last_face}
        return render(request, "ResidentManagement/ajax.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def scan(request):
    if request.user.is_authenticated:
        global last_face
        global detected_face

        known_face_encodings = []
        known_face_names = []

        profiles = ResidentsInfo.objects.all()
        for profile in profiles:
            person = profile.image
            image_of_person = face_recognition.load_image_file(f"media/{person}")
            person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
            known_face_encodings.append(person_face_encoding)
            known_face_names.append(f"{person}"[18:-4])

        video_capture = cv2.VideoCapture(0)

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, 0.4
                    )
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                        # if last_face != name:

                        #     # last_face = LastFace(last_face=name)
                        #     last_face = LastFace.objects.all().last()
                        #     if last_face == None:
                        #         last_face = LastFace(last_face=name)
                        #         last_face.save()
                        #     else:

                        #         last_face.last_face = name
                        #         last_face.save()
                        #     last_face = name
                        #     winsound.PlaySound(sound, winsound.SND_ASYNC)

                        # else:
                        #     pass

                        if last_face != name:
                            last_face = LastFace(last_face=name)
                            last_face.save()
                            last_face = name
                            winsound.PlaySound(sound, winsound.SND_ASYNC)

                        else:
                            pass

                    face_names.append(name)
                    # detected_face = DetectedFace(detected_face="face-detected")
                    # detected_face.save()

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1
                )

            cv2.imshow("Video", frame)
            cv2.setWindowProperty("Video", cv2.WND_PROP_TOPMOST, 1)
            if cv2.waitKey(1) & 0xFF == 13:
                break
            if cv2.getWindowProperty("Video", 0) < 0:
                break

        video_capture.release()
        cv2.destroyAllWindows()
        return HttpResponse("scaner closed", last_face)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def details(request):
    if request.user.is_authenticated:
        try:
            last_face = LastFace.objects.last()
            profile = ResidentsInfo.objects.get(Q(image__icontains=last_face))
        except:
            last_face = None
            profile = None

        context = {"profile": profile, "last_face": last_face, "clearance": clearance}
        return render(request, "ResidentManagement/details.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def add_profile(request):
    if request.user.is_authenticated:
        form = ProfileForm

        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            email = request.POST.get("email")

            filename = firstname + " " + lastname

            if form.is_valid():
                randomNum = User.objects.make_random_password(
                    length=2, allowed_chars="01234567889"
                )
                random_password = User.objects.make_random_password(
                    length=8, allowed_chars="01234567889"
                )
                username = f"{firstname.lower()}.{lastname.lower()}"

                user = User.objects.create_user(
                    email=email, username=username, password=random_password
                )
                group = Group.objects.get(name="resident")
                user.groups.add(group)

                subject = "Welcome to Barangay E-Service System!"
                message = f"""
                Dear {username},

                We are excited to have you on board and look forward to helping you access and manage the services offered by our platform.

                Here are your account details:
                Username: {user.username}
                Password: {random_password}

                Please keep this information safe and secure. 
                We recommend changing your password after logging in for the first time to enhance the security of your account.
                If you have any questions or concerns, please do not hesitate to contact us at the following numbers:            
                Globe: 09361174734
                TM: 09057198345
                
                Thank you for choosing Barangay E-Service System. We look forward to serving you.

                Best regards,
                The Barangay E-Service Team
                """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)

                resident = form.save(commit=False)
                resident.image.name = filename + ".jpg"
                resident.user = user
                resident.save()

                return redirect("resident_list")

        context = {"form": form}
        return render(request, "ResidentManagement/add_resident.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def edit_profile(request, id):
    if request.user.is_authenticated:
        profile = ResidentsInfo.objects.get(user=id)
        profile2 = User.objects.get(id=id)
        form2 = EditUserAccountForm(instance=profile2)
        form = ProfileForm(instance=profile)

        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            form2 = EditUserAccountForm(request.POST, instance=profile2)
            if form2.is_valid():
                form2.save()
                return redirect("resident_list")

            img = request.POST.get("image")
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            filename = firstname + " " + lastname

            if form.is_valid():
                if img == None:
                    userupdate = form.save(commit=False)
                    userupdate.image.name = filename + ".jpg"
                    userupdate.save()

                form.save()
                return redirect("resident_list")

        context = {"form": form, "form2": form2, "prev_img": profile.image}
        return render(request, "ResidentManagement/edit_resident.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def delete_profile(request, id):
    if request.user.is_authenticated:
        profile = User.objects.get(id=id)
        context = {"profile": profile}
        if request.method == "POST":
            if len(profile.residentsinfo.image) > 0:
                os.remove(profile.residentsinfo.image.path)
                profile.delete()
                return redirect("resident_list")
        return render(request, "ResidentManagement/delete_resident.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def view_profile(request, id):
    if request.user.is_authenticated:
        profile = User.objects.get(pk=id)
        context = {"profile": profile}
        return render(request, "ResidentManagement/view_profile.html", context)
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def profile_clearance(request, id):
    if request.user.is_authenticated:
        context = {"profile_clearance": clearance_list.objects.filter(res_id=id)}
        return render(
            request, "ResidentManagement/DocumentList/clearance_list.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def profile_indigency(request, id):
    if request.user.is_authenticated:
        context = {
            "profile_indigency": CertificateOfIndigency.objects.filter(res_id=id)
        }
        return render(
            request, "ResidentManagement/DocumentList/indigency_list.html", context
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def profile_business_permit(request, id):
    if request.user.is_authenticated:
        context = {"profile_business_permit": BusinessPermit.objects.filter(res_id=id)}
        return render(
            request,
            "ResidentManagement/DocumentList/business_permit_list.html",
            context,
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def profile_building_permit(request, id):
    if request.user.is_authenticated:
        context = {"building_permit_list": BuildingPermit.objects.filter(res_id=id)}
        return render(
            request,
            "ResidentManagement/DocumentList/building_permit_list.html",
            context,
        )
    else:
        return redirect("loginPage")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="loginPage")
@admin_only
def profile_residency_certificate(request, id):
    context = {
        "residency_certificate_list": ResidencyCertificate.objects.filter(res_id=id)
    }
    return render(
        request, "ResidentManagement/DocumentList/residency_certificate.html", context
    )


def print_data(request, id):
    template_name = "ResidentManagement/info-pdf.html"
    profile = User.objects.get(pk=id)
    return render_to_pdf(
        template_name,
        {
            "profile": profile,
        },
    )


# Process Document


def process_barangay_clearance(request, id):
    if request.user.is_authenticated:
        form = ProcessClearanceForm
        profile = User.objects.get(residentsinfo__pk=id)

        userid = ResidentsInfo.objects.get(id=id)

        status = DocumentStatus.objects.get(pk=3)

        if request.method == "POST":
            form = ProcessClearanceForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.res_id = userid
                instance.status = status
                instance.date_released = datetime.date.today()
                instance.save()
                return redirect(reverse("success_clearance", kwargs={"user_id": id}))

        context = {"profile": profile, "form": form}
        return render(
            request,
            "ResidentManagement/ProcessDocument/process_clearance.html",
            context,
        )
    else:
        return redirect("loginPage")


def success_clearance(request, user_id):
    profile = User.objects.get(residentsinfo__pk=user_id)

    context = {
        "profile": profile,
        "clearance": clearance_list.objects.filter(res_id=user_id).order_by("-id")[:1],
    }
    return render(
        request, "ResidentManagement/ProcessDocument/success_clearance.html", context
    )


def process_indigency(request, id):
    if request.user.is_authenticated:
        form = ProcessIndigencyForm
        profile = User.objects.get(residentsinfo__pk=id)
        userid = ResidentsInfo.objects.get(id=id)
        status = DocumentStatus.objects.get(pk=3)

        if request.method == "POST":
            form = ProcessIndigencyForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.res_id = userid
                instance.status = status
                instance.date_released = datetime.date.today()
                instance.save()
                return redirect(reverse("success_indigency", kwargs={"user_id": id}))

        context = {"profile": profile, "form": form}
        return render(
            request,
            "ResidentManagement/ProcessDocument/process_indigency.html",
            context,
        )
    else:
        return redirect("loginPage")


def success_indigency(request, user_id):
    profile = User.objects.get(residentsinfo__pk=user_id)

    context = {
        "profile": profile,
        "indigency": CertificateOfIndigency.objects.filter(res_id=user_id).order_by(
            "-id"
        )[:1],
    }
    return render(
        request, "ResidentManagement/ProcessDocument/success_indigency.html", context
    )


def process_BusinessPermit(request, id):
    if request.user.is_authenticated:
        form = ProcessBusinessPermitForm
        profile = User.objects.get(residentsinfo__pk=id)
        userid = ResidentsInfo.objects.get(id=id)
        status = DocumentStatus.objects.get(pk=3)
        owner = (
            userid.firstname
            + " "
            + userid.middlename
            + " "
            + userid.suffix
            + " "
            + userid.lastname
        )

        if request.method == "POST":
            form = ProcessBusinessPermitForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.res_id = userid
                instance.status = status
                instance.owner = owner
                instance.save()
                return redirect(reverse("success_business", kwargs={"user_id": id}))

        context = {"profile": profile, "form": form}
        return render(
            request,
            "ResidentManagement/ProcessDocument/process_BusinessPermit.html",
            context,
        )
    else:
        return redirect("loginPage")


def success_business(request, user_id):
    profile = User.objects.get(residentsinfo__pk=user_id)

    context = {
        "profile": profile,
        "BusinessPermit": BusinessPermit.objects.filter(res_id=user_id).order_by("-id")[
            :1
        ],
    }
    return render(
        request, "ResidentManagement/ProcessDocument/success_business.html", context
    )


def process_BuildingPermit(request, id):
    if request.user.is_authenticated:
        form = ProcessBuildingPermitForm
        profile = User.objects.get(residentsinfo__pk=id)
        userid = ResidentsInfo.objects.get(id=id)
        status = DocumentStatus.objects.get(pk=3)
        owner = (
            userid.firstname
            + " "
            + userid.middlename
            + " "
            + userid.suffix
            + " "
            + userid.lastname
        )

        if request.method == "POST":
            form = ProcessBuildingPermitForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.res_id = userid
                instance.status = status
                instance.owner = owner
                instance.save()
                return redirect(reverse("success_building", kwargs={"user_id": id}))

        context = {"profile": profile, "form": form}
        return render(
            request,
            "ResidentManagement/ProcessDocument/process_BuildingPermit.html",
            context,
        )
    else:
        return redirect("loginPage")


def success_building(request, user_id):
    profile = User.objects.get(residentsinfo__pk=user_id)

    context = {
        "profile": profile,
        "BuildingPermit": BuildingPermit.objects.filter(res_id=user_id).order_by("-id")[
            :1
        ],
    }
    return render(
        request, "ResidentManagement/ProcessDocument/success_building.html", context
    )


def process_ResidencyCertificate(request, id):
    if request.user.is_authenticated:
        form = ProcessResidencyCertificateForm
        profile = User.objects.get(residentsinfo__pk=id)
        userid = ResidentsInfo.objects.get(id=id)
        status = DocumentStatus.objects.get(pk=3)

        if request.method == "POST":
            form = ProcessResidencyCertificateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.res_id = userid
                instance.status = status
                instance.date_released = datetime.date.today()
                instance.save()
                return redirect(reverse("success_residency", kwargs={"user_id": id}))

        context = {"profile": profile, "form": form}
        return render(
            request,
            "ResidentManagement/ProcessDocument/process_ResidencyCertificate.html",
            context,
        )
    else:
        return redirect("loginPage")


def success_residency(request, user_id):
    profile = User.objects.get(residentsinfo__pk=user_id)

    context = {
        "profile": profile,
        "Residency": ResidencyCertificate.objects.filter(res_id=user_id).order_by(
            "-id"
        )[:1],
    }
    return render(
        request, "ResidentManagement/ProcessDocument/success_residency.html", context
    )
