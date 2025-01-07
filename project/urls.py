from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("BESS/", include("apps.Dashboard.urls")),
    path("BESS/", include("apps.AdminProfile.urls")),
    path("Poblacion/", include("apps.ResidentManagement.urls")),
    path("BESS/", include("apps.ClearanceManagement.urls")),
    path("BESS/", include("apps.IndigencyManagement.urls")),
    path("BESS/", include("apps.BusinessPermit.urls")),
    path("BESS/", include("apps.BuildingPermit.urls")),
    path("BESS/", include("apps.ResidencyCertificate.urls")),
    path("BESS/", include("apps.AnnouncementManagement.urls")),
    path("BESS/", include("apps.ReportManagement.urls")),
    path("BESS/", include("apps.RegisterOfficial.urls")),
    path("BESS/", include("apps.OfficialList.urls")),
    path("BESS/", include("apps.LoggedReports.urls")),
    path("BESS/", include("apps.RequestLogs.urls")),
    path("", include("apps.Login.urls")),
    path("", include("apps.UserPortal.urls")),
    # old urls
    # path('login/',include('apps.Login.urls')),
    # path('Barangay Poblacion/',include('apps.UserPortal.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
