from django.apps import AppConfig

NAME = "api.inventory"

class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = NAME
