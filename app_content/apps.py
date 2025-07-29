from django.apps import AppConfig


class AppContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_content"
    verbose_name = "Управление контентом"

    def ready(self):
        import app_content.signals.article_signals
