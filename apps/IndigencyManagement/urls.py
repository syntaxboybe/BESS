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
    path("delete_indigency/<hashid:id>", delete_indigency, name="delete_indigency"),
    path(
        "sign_indigency_cert/<hashid:id>/",
        sign_indigency_cert,
        name="sign_indigency_cert",
    ),
    path(
        "no_sign_indigencycert/<hashid:id>/",
        no_sign_indigencycert,
        name="no_sign_indigencycert",
    ),
]
