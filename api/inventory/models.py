from django.db import models

# Create your models here.


class Product(models.Model):
    """
    商品
    """

    name = models.CharField(max_length=100, verbose_name="商品名")
    price = models.IntegerField(verbose_name="価格")
    description = models.TextField(verbose_name="商品説明", null=True, blank=True)

    class Meta:
        db_table = "product"
        verbose_name = "商品"
