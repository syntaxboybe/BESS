from django.urls import path
from .views import *

from project.utils import HashIdConverter
from django.urls import register_converter

register_converter(HashIdConverter, "hashid")


urlpatterns = [
    path(
        "building_permit_request/",
        building_permit_module,
        name="building_permit_module",
    ),
    path("building_permit_list/", building_permit_list,
         name="building_permit_list"),
    path(
        "building_permit_list/<int:id>",
        edit_building_permit,
        name="edit_building_permit",
    ),
    path(
        "generate_building_permit/<hashid:id>",
        generate_building_permit,
        name="generate_building_permit",
    ),
    path(
        "delete_building_permit/<hashid:id>",
        delete_building_permit,
        name="delete_building_permit",
    ),
    path(
        "unsign_building_permit/<hashid:id>/",
        unsign_building_permit,
        name="unsign_building_permit",
    ),
    path(
        "no_sign_buildingpermit/<hashid:id>/",
        no_sign_buildingpermit,
        name="no_sign_buildingpermit",
    ),
    path(
        "esign_building_permit/<hashid:id>/",
        esign_building_permit,
        name="esign_building_permit",
    ),
    path(
        "confirm_button_bldp/<hashid:id>/",
        confirm_button_bldp,
        name="confirm_button_bldp",
    ),
    path(
        "esign_button_bldp/<hashid:id>/",
        esign_button_bldp,
        name="esign_button_bldp",
    ),
    path(
        "release_unsign_bldp/<hashid:id>/",
        release_unsign_bldp,
        name="release_unsign_bldp",
    ),
    path(
        "release_esigned_bldp/<hashid:id>/",
        release_esigned_bldp,
        name="release_esigned_bldp",
    ),
]
