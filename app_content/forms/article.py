from django import forms

from django.utils.translation import gettext_lazy as _

from parler.forms import TranslatableModelForm

from app_content.models.article import Article


class ArticleAdminForm(TranslatableModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk and self.request:
            self.fields["author"].initial = self.request.user

    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(
                attrs={"style": "width: 100%; height: 40px; padding: 5px;"}
            ),
            "slug": forms.TextInput(
                attrs={
                    "style": "width: 100%; height: 40px; padding: 5px;",
                    "placeholder": "Заполняется автоматически из Заголовка статьи",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "style": (
                        "width: 100%; "  # на всю ширину контейнера
                        "height: 200px; "  # увеличиваем высоту
                        "resize: vertical; "  # разрешаем тянуть вниз мышкой
                        "font-family: Arial, sans-serif; "  # нормальный шрифт
                        "font-size: 14px; "  # читаемый размер
                        "line-height: 1.5;"  # комфортное межстрочное расстояние
                    ),
                    "rows": 10,
                    "placeholder": "Введите краткое описание статьи...",
                }
            ),
        }
