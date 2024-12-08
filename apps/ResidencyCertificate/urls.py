from django.urls import path
from .views import *
from project.utils import HashIdConverter
from django.urls import register_converter

register_converter(HashIdConverter, "hashid")


urlpatterns = [
    path(
        "residency_request/",
        residency_certificate_module,
        name="residency_certificate_module",
    ),
    path("residency/", residency_certificate_list, name="residency_certificate_list"),
    path("residency/<int:id>", edit_residency, name="edit_residency"),
    path(
        "generate_resident_certificate/<hashid:id>",
        generate_resident_certificate,
        name="generate_resident_certificate",
    ),
    path(
        "delete_resident_certificate_request/<hashid:id>",
        delete_resident_certificate_request,
        name="delete_resident_certificate_request",
    ),
    path(
        "unsign_residency_cert/<hashid:id>/",
        unsign_residency_cert,
        name="unsign_residency_cert",
    ),
    path(
        "no_sign_residencycert/<hashid:id>/",
        no_sign_residencycert,
        name="no_sign_residencycert",
    ),
    path(
        "esign_residency_cert/<hashid:id>/",
        esign_residency_cert,
        name="esign_residency_cert",
    ),
]
