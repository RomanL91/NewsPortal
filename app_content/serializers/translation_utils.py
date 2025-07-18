from django.conf import settings
from parler.utils.context import switch_language


class TranslationAwareSerializerMixin:
    """
    Миксин для сериализаторов, обеспечивающий:
    - определение языка из запроса
    - извлечение перевода из parler-safe методов
    """

    def get_lang(self):
        request = self.context.get("request") if hasattr(self, "context") else None
        return getattr(
            request, "LANGUAGE_CODE", getattr(settings, "LANGUAGE_CODE", "ru")
        )

    def get_translated(self, obj, field_name: str):
        lang = self.get_lang()
        with switch_language(obj, lang):
            return obj.safe_translation_getter(field_name, default=None)


def create_translated_getter(field_name: str):
    """
    Создаёт метод get_<field_name>, возвращающий перевод поля.
    Пример использования:
        get_name = create_translated_getter("name")
    """

    def getter(self, obj):
        return self.get_translated(obj, field_name)

    getter.__name__ = f"get_{field_name}"
    return getter
