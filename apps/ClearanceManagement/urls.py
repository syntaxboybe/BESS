from django.urls import path, include
from .views import *
from project.utils import HashIdConverter
from django.urls import register_converter
from django.conf import settings
from django.conf.urls.static import static

register_converter(HashIdConverter, "hashid")


urlpatterns = [
    path("clearance/", clearance, name="clearance"),
    path("clearance/<int:id>", edit_clearance, name="edit_clearance"),
    path("clearance_list", clearance_list, name="clearance_list"),
    path(
        "generate_clearance/<hashid:id>/", generate_clearance, name="generate_clearance"
    ),
    path("delete_clearance/<hashid:id>",
         delete_clearance, name="delete_clearance"),
    path("esign_clearance/<hashid:id>/",
         esign_clearance, name="esign_clearance"),
    path("no_sign_clearance/<hashid:id>/",
         no_sign_clearance, name="no_sign_clearance"),
    path("unsign_clearance/<hashid:id>/",
         unsign_clearance, name="unsign_clearance"),
    path("esign_button/<hashid:id>/", esign_button, name="esign_button"),
    path("confirm_button/<hashid:id>/", confirm_button, name="confirm_button"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
