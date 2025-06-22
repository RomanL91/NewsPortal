from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reversion.admin import VersionAdmin
from parler.admin import TranslatableAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from app_content.models.tag import Tag
from app_content.models.article import Article
from app_content.models.category import Category

from app_content.forms.tag import TagAdminForm
from app_content.forms.article import ArticleAdminForm
from app_content.forms.category import CategoryAdminForm


@admin.register(Article)
class ArticleAdmin(TranslatableAdmin, VersionAdmin):
    form = ArticleAdminForm

    list_display = ("title", "status", "author", "published_at")
    list_filter = ("status", "category", "tags")
    search_fields = (
        "translations__title",
        "translations__slug",
        "translations__summary",
    )
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "category", "content")}),
        (_("Мета"), {"fields": ("status", "tags")}),
        (_("Тайм-стемпы"), {"fields": ("published_at",), "classes": ("collapse",)}),
        (_("Автор"), {"fields": ("author",)}),
    )


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, DjangoMpttAdmin):
    form = CategoryAdminForm

    list_display = (
        "name",
        "slug",
    )

    prepopulated_fields = {}

    search_fields = ("translations__name", "translations__slug")
    list_filter = (("parent", admin.RelatedOnlyFieldListFilter),)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(TranslatableAdmin):
    form = TagAdminForm
    prepopulated_fields = {}
    list_display = ("name", "slug")
    search_fields = ("translations__name", "translations__slug")

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
