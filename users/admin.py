from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from django.utils.html import format_html

from .models import User, Role


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # добавляем колонку phone
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "phone",
                    "photo",
                )
            },
        ),
    )

    # отображение колонки с превью фото
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                f'<img src="{obj.photo.url}" style="height: 40px; border-radius: 4px;" />'
            )
        return "-"

    photo_preview.short_description = "Фото"
    list_display = (
        "photo_preview",
        *DjangoUserAdmin.list_display,
        "phone",
    )
    search_fields = (*DjangoUserAdmin.search_fields, "phone")


admin.site.unregister(Group)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ("permissions",)
