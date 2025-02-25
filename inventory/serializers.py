from rest_framework import serializers
from .models import ComponentCategory
from inventory.models import CheapItem, ExpensiveItem
from inventory.models import ComponentCategory
class ComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = '__all__'  # Includes all model fields


class CheapItemAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheapItem
        fields = '__all__'

class CheapItemDetailSerializer(serializers.ModelSerializer):
    category = ComponentCategorySerializer()

    class Meta:
        model = CheapItem
        fields = [
            "component_id",
            "name",
            "category",
            "stock",
            "description",
            "quantity_available",
            "weight",
            "max_time",
            "requires_admin_approval",
            "image",
        ]


class ExpensiveItemAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensiveItem
        fields = '__all__'

class CheapItemListSerializer(serializers.ModelSerializer):
    category = ComponentCategorySerializer()

    class Meta:
        model = CheapItem
        fields = ['component_id', 'name', 'category', 'stock', 'quantity_available', 'weight', 'image']

class ExpensiveItemListSerializer(serializers.ModelSerializer):
    category = ComponentCategorySerializer()

    class Meta:
        model = ExpensiveItem
        fields = ['component_id', 'name', 'category', 'stock', 'quantity_available', 'weight', 'image']
        
class CombinedItemSerializer(serializers.Serializer):
    component_id = serializers.UUIDField()
    name = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=ComponentCategory.objects.all(), allow_null=True)
    stock = serializers.IntegerField()
    quantity_available = serializers.IntegerField()
    weight = serializers.FloatField()
    image = serializers.CharField()
    item_type = serializers.SerializerMethodField()

    def get_item_type(self, obj):
        if isinstance(obj, CheapItem):
            return "cheap"
        elif isinstance(obj, ExpensiveItem):
            return "expensive"
        return "unknown"
