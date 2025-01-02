from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Poblacion/", include("apps.Dashboard.urls")),
    path("Poblacion/", include("apps.AdminProfile.urls")),
    path("Poblacion/", include("apps.ResidentManagement.urls")),
    path("Poblacion/", include("apps.ClearanceManagement.urls")),
    path("Poblacion/", include("apps.IndigencyManagement.urls")),
    path("Poblacion/", include("apps.BusinessPermit.urls")),
    path("Poblacion/", include("apps.BuildingPermit.urls")),
    path("Poblacion/", include("apps.ResidencyCertificate.urls")),
    path("Poblacion/", include("apps.AnnouncementManagement.urls")),
    path("Poblacion/", include("apps.ReportManagement.urls")),
    path("Poblacion/", include("apps.RegisterOfficial.urls")),
    path("Poblacion/", include("apps.OfficialList.urls")),
    path("Poblacion/", include("apps.LoggedReports.urls")),
    path("Poblacion/", include("apps.RequestLogs.urls")),
    path("", include("apps.Login.urls")),
    path("", include("apps.UserPortal.urls")),
    # old urls
    # path('login/',include('apps.Login.urls')),
    # path('Barangay Poblacion/',include('apps.UserPortal.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
