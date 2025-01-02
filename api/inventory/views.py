from django.db.models import F
from django.db.models import Sum
from django.db.models import Value
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from api.inventory.exception import BusinessException
from api.inventory.models import Product
from api.inventory.models import Purchase
from api.inventory.models import Sales
from api.inventory.serializers import InventorySerializer
from api.inventory.serializers import ProductSerializer
from api.inventory.serializers import PurchaseSerializer
from api.inventory.serializers import SalesSerializer


class InventoryView(views.APIView):
    """在庫操作に関する関数"""

    def get(self, request: Request, _id: int | None = None, format=None) -> Response:
        """仕入れ、売上情報を取得する"""
        if _id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        purchase = (
            Purchase.objects.filter(product_id=_id)
            .prefetch_related("product")
            .values(
                "id",
                "quantity",
                type=Value("1"),
                date=F("purchase_date"),
                unit=F("product__price"),
            )
        )
        sales = (
            Sales.objects.filter(product_id=_id)
            .prefetch_related("product")
            .values(
                "id",
                "quantity",
                type=Value("2"),
                date=F("sales_date"),
                unit=F("product__price"),
            )
        )
        queryset = purchase.union(sales).order_by(F("date"))
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(views.APIView):
    """商品操作に関する関数"""

    def __init__(self) -> None:
        super().__init__()
        self._serializer = ProductSerializer

    def get_object(self, primary_key: int) -> Product:
        """idとprimary_keyが一致する1つの商品を取得する"""
        try:
            return Product.objects.get(pk=primary_key)
        except Product.DoesNotExist as e:
            raise NotFound from e

    def get(self, request: Request, _id: int | None = None, format=None) -> Response:
        """商品一覧、もしくは一意の商品を取得する"""
        if _id is None:
            queryset = Product.objects.all()
            serializer = self._serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        product = self.get_object(_id)
        serializer = self._serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, format=None) -> Response:
        """商品を新規登録する"""
        serializer = self._serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request: Request, _id: int, format=None) -> Response:
        """登録済みの商品を更新する"""
        product = self.get_object(_id)
        serializer = self._serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, _id: int, format=None) -> Response:
        """登録済みの商品を削除する"""
        product = self.get_object(_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductModelViewSet(viewsets.ModelViewSet):
    """商品操作に関する関数（ModelViewSet）"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseView(views.APIView):
    """仕入操作に関する関数"""

    def post(self, request: Request, format=None) -> Response:
        """仕入情報を登録する"""
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SalesView(views.APIView):
    """売上操作に関する関数"""

    def post(self, request: Request, format=None) -> Response:
        """売上情報を登録する"""
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._check_quantity_is_over(request)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _check_quantity_is_over(self, request: Request) -> None:
        """売る分の数量が在庫を超えないかチェック"""
        # 在庫テーブルのレコードを取得
        purchase = Purchase.objects.filter(
            product_id=request.data["product"]
        ).aggregate(quantity_sum=Coalesce(Sum("quantity"), 0))

        # 卸しテーブルのレコードを取得
        sales = Sales.objects.filter(product_id=request.data["product"]).aggregate(
            quantity_sum=Coalesce(Sum("quantity"), 0)
        )

        stock = purchase["quantity_sum"] - sales["quantity_sum"]
        is_over = stock < int(request.data["quantity"])
        if is_over:
            errmsg = "在庫数量を超過することはできません"
            raise BusinessException(errmsg)
