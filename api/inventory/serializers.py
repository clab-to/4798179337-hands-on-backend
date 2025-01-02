from rest_framework import serializers

from api.inventory.models import Product
from api.inventory.models import Purchase
from api.inventory.models import Sales


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
