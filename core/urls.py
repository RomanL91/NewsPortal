from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# # во время разработки отдаём медиафайлы напрямую
# if settings.DEBUG:
#     urlpatterns
#     +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "Новостной портал (СМИ)"
admin.site.index_title = "Новостной портал (СМИ)"  # default: "Site administration"
admin.site.site_title = "Новостной портал (СМИ)"  # default: "Django site admin"
admin.site.site_url = None
# admin.site.disable_action('delete_selected')
