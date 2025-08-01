from django.contrib import admin
from django.utils.timezone import localtime
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from reversion.models import Version
from reversion.admin import VersionAdmin
from parler.admin import TranslatableAdmin
from parler.utils.context import get_language
from django_mptt_admin.admin import DjangoMpttAdmin

from app_content.models.tag import Tag
from app_content.models.article import Article
from app_content.models.category import Category

from app_content.forms.tag import TagAdminForm
from app_content.forms.article import ArticleAdminForm
from app_content.forms.category import CategoryAdminForm


class TagLanguageAwareFilter(SimpleListFilter):
    title = _("теги")
    parameter_name = "tags__id__exact"

    def lookups(self, request, model_admin):
        lang = getattr(request, "LANGUAGE_CODE", get_language() or "ru")
        tags = Tag.objects.language(lang).order_by("id").distinct("id")
        return [(tag.id, tag.safe_translation_getter("name")) for tag in tags]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(tags__id=value)
        return queryset


@admin.register(Article)
class ArticleAdmin(TranslatableAdmin, VersionAdmin, admin.ModelAdmin):
    form = ArticleAdminForm

    readonly_fields = (
        "views_count",
        "cover_preview",
        "thumbnail_preview",
        "article_history_display",
        "created_at",
        "updated_at",
    )
    list_display = (
        "title",
        "status",
        "published_at",
        "author",
        "views_count",
        "thumbnail_preview",
        # "cover_preview",
    )
    list_filter = (
        "status",
        "category",
        TagLanguageAwareFilter,
    )
    search_fields = (
        "translations__title",
        "translations__slug",
        "translations__summary",
    )
    date_hierarchy = "created_at"
    autocomplete_fields = ("tags", "category")

    def cover_preview(self, obj):
        if obj.cover_image:
            return mark_safe(
                f'<img src="{obj.cover_image.url}" style="max-height: 200px;" />'
            )
        return "-"

    cover_preview.short_description = "Превью обложки"

    def thumbnail_preview(self, obj):
        if obj.cover_thumbnail:
            return mark_safe(
                f"<img src='{obj.cover_thumbnail.url}' style='max-height: 100px;' />"
            )
        return "-"

    thumbnail_preview.short_description = "Миниатюра"
    thumbnail_preview.allow_tags = True

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",)}

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = self.form
        form = super().get_form(request, obj, **kwargs)

        # передаем request в форму
        class FormWithRequest(form):
            def __new__(cls, *args, **kw):
                kw["request"] = request
                return form(*args, **kw)

        return FormWithRequest

    def article_history_display(self, obj):
        if not obj.pk:
            return "Статья ещё не сохранена."

        versions = Version.objects.get_for_object(obj)
        if versions.count() < 2:
            return "Нет истории изменений."

        IGNORE_FIELDS = {"cover_thumbnail", "updated_at", "created_at", "id"}

        lines = []
        versions = list(versions)

        for i in range(len(versions) - 1):
            current = versions[i]
            previous = versions[i + 1]

            diffs = []
            for key in current.field_dict:
                if key in IGNORE_FIELDS:
                    continue
                old = previous.field_dict.get(key)
                new = current.field_dict.get(key)
                if old != new:
                    diffs.append(f"  • {key}: {old} → {new}")

            if diffs:
                user = current.revision.user or "Неизвестно"
                time = localtime(current.revision.date_created).strftime(
                    "%Y-%m-%d %H:%M"
                )
                lines.append(f"{user} — {time}\n" + "\n".join(diffs))

        return (
            mark_safe("<pre>" + "\n\n".join(lines) + "</pre>")
            if lines
            else "Изменений не найдено."
        )

    article_history_display.short_description = "История изменений"

    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": (
                    "title",
                    "slug",
                    "summary",
                    "status",
                    "author",
                    "published_at",
                )
            },
        ),
        (_("Контент"), {"fields": ("content",)}),
        (
            _("Изображения"),
            {
                "fields": (
                    "cover_image",
                    "cover_preview",
                    # "thumbnail_preview",
                )
            },
        ),
        (_("Категории и теги"), {"fields": ("category", "tags")}),
        (
            _("Системные данные"),
            {
                "classes": ("collapse",),
                "fields": (
                    "views_count",
                    "article_history_display",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
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

    def get_queryset(self, request):
        lang = getattr(request, "LANGUAGE_CODE", "ru")
        return (
            super().get_queryset(request).language(lang).order_by("id").distinct("id")
        )

    def get_search_results(self, request, queryset, search_term):
        lang = getattr(request, "LANGUAGE_CODE", "ru")
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.language(lang).order_by("id").distinct("id")
        return queryset, use_distinct
