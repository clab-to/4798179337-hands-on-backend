from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from api.inventory import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("retry/", views.RetryView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("products/", views.ProductView.as_view()),
    path("products/<int:_id>/", views.ProductView.as_view()),
    path(
        "products/model/",
        views.ProductModelViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path("inventories/<int:_id>/", views.InventoryView.as_view()),
    path("purchases/", views.PurchaseView.as_view()),
    path("sales/", views.SalesView.as_view()),
]
