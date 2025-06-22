from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableManager, TranslatableQuerySet


class TranslatableTreeQuerySet(TranslatableQuerySet, TreeQuerySet):
    """QuerySet, понимающий и parler, и mptt."""

    pass


class TranslatableTreeManager(TreeManager, TranslatableManager):
    _queryset_class = TranslatableTreeQuerySet


class Category(TranslatableModel, MPTTModel):
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    translations = TranslatedFields(
        name=models.CharField(_("название"), max_length=120),
        slug=models.SlugField(unique=False),
    )

    objects = TranslatableTreeManager()

    class MPTTMeta:
        pass

    class Meta:
        verbose_name = _("рубрика")
        verbose_name_plural = _("рубрики")

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)
