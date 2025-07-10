from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
        path("i18n/", include("django.conf.urls.i18n")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + i18n_patterns(
        path("", include("app_content.urls")),  # или как называется твоё приложение
    )
)

# Настройки DEBUG для TailWind
if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

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
