import re
from urllib.parse import urljoin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_content.models.article import Article


@receiver(post_save, sender=Article)
def force_absolute_media_links_in_content(sender, instance: Article, **kwargs):
    """
    После сохранения статьи заменяет src="/media/..." на абсолютные ссылки
    во всех переводах content через translation.save().
    """
    base_url = getattr(settings, "SITE_URL", "").rstrip("/")

    for lang_code in instance.get_available_languages():
        try:
            translation = instance.get_translation(language_code=lang_code)
            content = translation.content
            if content and "/media/" in content:
                updated = re.sub(
                    r'src=[\'"](/media/[^\'"]+)[\'"]',
                    lambda m: f'src="{urljoin(base_url + "/", m.group(1))}"',
                    content,
                )
                if updated != content:
                    translation.content = updated
                    translation.save(update_fields=["content"])
        except Exception as e:
            print(
                f"[!] Ошибка обработки перевода ({lang_code}) статьи {instance.pk}: {e}"
            )
