from rest_framework import serializers
from core.models import Status, TxType, Category, SubCategory
from cashflow.models import CashFlowEntry

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class TxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TxType
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class CashFlowEntrySerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    type = TxTypeSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = CashFlowEntry
        fields = ['id', 'created_at', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']

    def validate(self, attrs):
        type_obj = attrs.get('type') or getattr(self.instance, 'type', None)
        category = attrs.get('category') or getattr(self.instance, 'category', None)
        subcategory = attrs.get('subcategory') or getattr(self.instance, 'subcategory', None)

        if category and type_obj and category.type_id != type_obj.id:
            raise serializers.ValidationError({'category': 'Категория не относится к выбранному типу.'})

        if subcategory and category and subcategory.category_id != category.id:
            raise serializers.ValidationError({'subcategory': 'Подкатегория не относится к выбранной категории.'})

        if not attrs.get('amount') and not getattr(self.instance, 'amount', None):
            raise serializers.ValidationError({'amount': 'Обязательное поле.'})

        return attrs
