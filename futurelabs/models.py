import json, datetime
from django.utils import timezone
from django.db import models

class ProductsDetails(models.Model):
    product_name = models.CharField(max_length=2048, null=True, blank=True)
    url = models.CharField(max_length=2048, null=True, unique=True)
    image_url = models.CharField(max_length=2048, null=True)
    cost = models.FloatField(null=True, default=0.0, blank=True)
    shipping_price = models.FloatField(null=True, default=0.0, blank=True)
    total_price = models.FloatField(null=True, default=0.0, blank=True)
    shipping_method = models.CharField(max_length=20, null=True, blank=True)
    arrive_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)