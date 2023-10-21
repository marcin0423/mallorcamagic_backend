from rest_framework.serializers import ModelSerializer
from .models import SavedGuide, SavedProperty


class GuideSerializer(ModelSerializer):
    class Meta:
        model = SavedGuide
        fields = ["slug", "thumbnail", "title_en", "short_desc_en", "long_desc_en"]


class PropertySerializer(ModelSerializer):
    class Meta:
        model = SavedProperty
        fields = ["slug", "thumbnail", "title", "bathrooms", "bedrooms", "area", "price_unit", "price_amount"]
