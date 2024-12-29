from django.urls import path
from .views import *


from project.utils import HashIdConverter
from django.urls import register_converter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path(
        "business_permit_request/",
        business_permit_module,
        name="business_permit_module",
    ),
    path("business_permit_list/", business_permit_list,
         name="business_permit_list"),
    path("businessPermit/<int:id>", edit_business_permit,
         name="edit_business_permit"),
    path(
        "generate_business_permit/<hashid:id>",
        generate_business_permit,
        name="generate_business_permit",
    ),
    path(
        "delete_business_permit/<hashid:id>",
        delete_business_permit,
        name="delete_business_permit",
    ),
    path(
        "unsign_business_permit/<hashid:id>/",
        unsign_business_permit,
        name="unsign_business_permit",
    ),
    path(
        "no_sign_businesspermit/<hashid:id>/",
        no_sign_businesspermit,
        name="no_sign_businesspermit",
    ),
    path(
        "esign_business_permit/<hashid:id>/",
        esign_business_permit,
        name="esign_business_permit",
    ),
    path(
        "confirm_button_bsp/<hashid:id>/",
        confirm_button_bsp,
        name="confirm_button_bsp",
    ),
    path(
        "esign_button_bsp/<hashid:id>/",
        esign_button_bsp,
        name="esign_button_bsp",
    ),
    path(
        "release_esigned_bsp/<hashid:id>/",
        release_esigned_bsp,
        name="release_esigned_bsp",
    ),
    path(
        "release_unsign_bsp/<hashid:id>/",
        release_unsign_bsp,
        name="release_unsign_bsp",
    ),
]
