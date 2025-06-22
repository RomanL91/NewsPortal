from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields


class Tag(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("название"), max_length=64, unique=True),
        slug=models.SlugField(_("slug"), max_length=64, unique=True),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("тег")
        verbose_name_plural = _("теги")
        ordering = ("translations__name",)

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)
