import os
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


def user_avatar_upload_path(instance, filename):
    return os.path.join("avatars", f"user_{instance.id}", filename)


class User(AbstractUser):
    """
    Базовая модель, полностью совместимая с Django,
    но позволяет спокойно добавлять поля в будущем.
    """

    # пример дополнительного поля
    phone = models.CharField(_("phone number"), max_length=20, blank=True)
    photo = models.ImageField(
        _("Фотография"),
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        default="avatars/avatar_default.png",  # положи default-картинку в MEDIA_ROOT/avatars/
    )

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
