from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect

from app_content.urls import urlpatterns as app_urls

urlpatterns = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("api/v1/", include(app_urls)),
    # редирект с /admin/ на /ru/admin/
    path("admin/", lambda request: redirect("/ru/admin/")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "SKO24"
admin.site.index_title = (
    "SKO24 - События. Мнения. Аналитика. (лозунг РБК)"  # default: "Site administration"
)
admin.site.site_title = "SKO24"  # default: "Django site admin"
