from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.inventory.models import Product
from api.inventory.serializers import ProductSerializer


class ProductView(views.APIView):
    """商品操作に関する関数"""

    def get(self, request: Request, format=None) -> Response:
        """商品一覧を取得する"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
