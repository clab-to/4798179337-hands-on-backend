from django.urls import path

from api.inventory.views import ProductModelViewSet
from api.inventory.views import ProductView
from api.inventory.views import PurchaseView
from api.inventory.views import SalesView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<int:_id>", ProductView.as_view()),
    path(
        "products/model", ProductModelViewSet.as_view({"get": "list", "post": "create"})
    ),
    path("purchases/", PurchaseView.as_view()),
    path("sales/", SalesView.as_view()),
]
