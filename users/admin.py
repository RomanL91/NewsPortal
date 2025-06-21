from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .models import User, Role


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # добавляем колонку phone
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("phone",)}),
    )
    list_display = (*DjangoUserAdmin.list_display, "phone")
    search_fields = (*DjangoUserAdmin.search_fields, "phone")


admin.site.unregister(Group)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ("permissions",)
