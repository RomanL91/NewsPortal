from parler.forms import TranslatableModelForm
from app_content.models.category import Category


class CategoryAdminForm(TranslatableModelForm):
    class Meta:
        model = Category
        fields = "__all__"
