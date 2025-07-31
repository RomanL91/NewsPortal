from rest_framework import serializers
from app_content.models.tag import Tag
from app_content.serializers.translation_utils import (
    TranslationAwareSerializerMixin,
    create_translated_getter,
)


class TagSerializer(TranslationAwareSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_name = create_translated_getter("name")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "created_at"]
