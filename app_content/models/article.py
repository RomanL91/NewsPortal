import os
import reversion

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields

from app_content.models.tag import Tag
from app_content.models.category import Category


def validate_image_size(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f"Размер изображения не должен превышать {max_size_mb} МБ."
        )


def validate_image_resolution(file):
    max_width = 1920
    max_height = 1080

    try:
        image = Image.open(file)
        width, height = image.size
        if width > max_width or height > max_height:
            raise ValidationError(
                f"Максимальное разрешение: {max_width}x{max_height}px."
            )
    except Exception as e:
        raise ValidationError(f"Не удалось обработать изображение. {e}")


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
    cover_image = models.ImageField(
        _("обложка"),
        upload_to="articles/covers/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
            validate_image_resolution,
        ],
    )
    cover_thumbnail = models.ImageField(
        _("миниатюра"),
        upload_to="articles/covers/thumbnails/",
        null=True,
        blank=True,
        editable=False,
    )
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
    views_count = models.PositiveIntegerField(
        _("кол-во просмотров"), default=0, editable=False
    )
    published_at = models.DateTimeField(_("дата публикации"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("статья")
        verbose_name_plural = _("статьи")
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сохраняем обложку
        if self.cover_image:
            self.resize_and_generate_thumbnail()

    def resize_and_generate_thumbnail(self):
        try:
            img = Image.open(self.cover_image)
            img = img.convert("RGB")

            # === resize оригинала ===
            max_size = (1200, 800)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size)

                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)

                file_name = os.path.basename(self.cover_image.name)
                self.cover_image.save(file_name, ContentFile(buffer.read()), save=False)

            # === thumbnail в webp ===
            thumb_size = (300, 200)
            img_thumb = Image.open(self.cover_image)
            img_thumb = img_thumb.convert("RGB")
            img_thumb.thumbnail(thumb_size)

            thumb_buffer = BytesIO()
            img_thumb.save(thumb_buffer, format="WEBP", quality=80)
            thumb_buffer.seek(0)

            base_name = os.path.splitext(os.path.basename(self.cover_image.name))[0]
            thumb_name = f"{base_name}_thumb.webp"

            self.cover_thumbnail.save(
                thumb_name, ContentFile(thumb_buffer.read()), save=False
            )

            # перезапись объекта
            super().save(update_fields=["cover_image", "cover_thumbnail"])

        except Exception as e:
            print(f"[!] Ошибка при обработке обложки: {e}")

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)
