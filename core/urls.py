from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]


admin.site.site_header = "Новостной портал (СМИ)"
admin.site.index_title = "Новостной портал (СМИ)"  # default: "Site administration"
admin.site.site_title = "Новостной портал (СМИ)"  # default: "Django site admin"
admin.site.site_url = None
# admin.site.disable_action('delete_selected')
