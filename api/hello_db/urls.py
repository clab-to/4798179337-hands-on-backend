from django.urls import path

from api.hello_db import views

urlpatterns = [path("backend/", views.Db.as_view())]
