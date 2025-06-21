from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Базовая модель, полностью совместимая с Django,
    но позволяет спокойно добавлять поля в будущем.
    """

    # пример дополнительного поля
    phone = models.CharField(_("phone number"), max_length=20, blank=True)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")


# ─────────────────────────────────────────────────────────────────────────────
# (необязательно) прокси-модель для групп, чтобы в admin можно было
# переименовать «Groups» → «Roles» и расширить форму
# ─────────────────────────────────────────────────────────────────────────────
class Role(Group):
    class Meta:
        proxy = True
        verbose_name = _("Группа")
        verbose_name_plural = _("Группы")
