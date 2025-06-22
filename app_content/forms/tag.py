from parler.forms import TranslatableModelForm
from app_content.models.tag import Tag


class TagAdminForm(TranslatableModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
