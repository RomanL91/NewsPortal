import reversion
from django.db import models
from django.utils.translation import gettext_lazy as _


@reversion.register()
class ArticleRevision(models.Model):
    """
    Чисто для admin-audit-trail: сохраняем снимок JSON-данных,
    кто и когда сделал правку. Storage – таблица reversion.
    """

    class Meta:
        proxy = True
        verbose_name = _("ревизия статьи")
        verbose_name_plural = _("ревизии статей")
