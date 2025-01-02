from rest_framework import serializers

from api.inventory.models import Product
from api.inventory.models import Purchase
from api.inventory.models import Sales


class InventorySerializer(serializers.Serializer):
    """在庫のシリアライザ

    仕入れ、売上情報の一覧。
    Modelに依存しないため、個別にフィールドを定義している
    """

    id = serializers.IntegerField()
    unit = serializers.IntegerField()
    quantity = serializers.IntegerField()
    type = serializers.IntegerField()
    date = serializers.DateTimeField()


class ProductSerializer(serializers.ModelSerializer):
    """商品のシリアライザ"""

    class Meta:
        model = Product
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    """仕入のシリアライザ"""

    class Meta:
        model = Purchase
        fields = "__all__"


class SalesSerializer(serializers.ModelSerializer):
    """売上のシリアライザ"""

    class Meta:
        model = Sales
        fields = "__all__"
