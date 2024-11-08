from django.urls import path

from api.hello import views

urlpatterns = [path("backend/", views.Backend.as_view())]
