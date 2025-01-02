from django.urls import path

from api.inventory.views import ProductModelViewSet
from api.inventory.views import ProductView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/model", ProductModelViewSet.as_view({"get": "list"})),
]
