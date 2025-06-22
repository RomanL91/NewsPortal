from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from parler.forms import TranslatableModelForm

from app_content.models.article import Article


class ArticleAdminForm(TranslatableModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "tags": admin.widgets.FilteredSelectMultiple(
                verbose_name=_("теги"),
                is_stacked=False,
            ),
            "category": admin.widgets.FilteredSelectMultiple(
                verbose_name=_("рубрики"),
                is_stacked=False,
            ),
        }
