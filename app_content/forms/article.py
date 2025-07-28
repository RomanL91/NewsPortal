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
