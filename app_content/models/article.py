import reversion

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields


from app_content.models.tag import Tag
from app_content.models.category import Category


@reversion.register()
class Article(TranslatableModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Черновик")
        REVIEW = "review", _("На модерации")
        PUBLISHED = "published", _("Опубликовано")
        ARCHIVED = "archived", _("В архиве")

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        verbose_name=_("теги"),
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name="articles",
        verbose_name=_("рубрики"),
    )

    # — переводимые поля —
    translations = TranslatedFields(
        title=models.CharField(_("заголовок"), max_length=250),
        slug=models.SlugField(_("slug"), max_length=250, unique=True),
        summary=models.TextField(_("краткое описание"), blank=True),
        content=CKEditor5Field(_("контент"), config_name="extends"),
    )

    # — непереводимые —
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="автор",
    )
    status = models.CharField(
        _("статус"), max_length=10, choices=Status.choices, default=Status.DRAFT
    )

    published_at = models.DateTimeField(_("дата публикации"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("статья")
        verbose_name_plural = _("статьи")
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)
