from django.urls import path
from .views import *
from project.utils import HashIdConverter
from django.urls import register_converter

register_converter(HashIdConverter, "hashid")


urlpatterns = [
    path("indigency_request/", indigency_module, name="indigency_request"),
    path("indigency/", indigency_list, name="indigency_list"),
    path("indigency/<int:id>", edit_indigency, name="edit_indigency"),
    path(
        "generate_indigency/<hashid:id>", generate_indigency, name="generate_indigency"
    ),
    path("delete_indigency/<hashid:id>",
         delete_indigency, name="delete_indigency"),
    path(
        "unsign_indigency_cert/<hashid:id>/",
        unsign_indigency_cert,
        name="unsign_indigency_cert",
    ),
    path(
        "no_sign_indigencycert/<hashid:id>/",
        no_sign_indigencycert,
        name="no_sign_indigencycert",
    ),
    path(
        "esign_indigency_cert/<hashid:id>/",
        esign_indigency_cert,
        name="esign_indigency_cert",
    ),
    path(
        "confirm_button_indigency/<hashid:id>/",
        confirm_button_indigency,
        name="confirm_button_indigency",
    ),
    path(
        "esign_button_indigency/<hashid:id>/",
        esign_button_indigency,
        name="esign_button_indigency",
    ),
    path(
        "release_esigned_indigency/<hashid:id>/",
        release_esigned_indigency,
        name="release_esigned_indigency",
    ),
    path(
        "release_unsign_indigency/<hashid:id>/",
        release_unsign_indigency,
        name="release_unsign_indigency",
    ),
]
