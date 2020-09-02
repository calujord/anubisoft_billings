from django.db import models


class BusinessBilling(models.Model):
    public_key = models.CharField(max_length=100, null=True, blank=True)
    secret_key = models.CharField(max_length=100, null=True, blank=True)
    establecimiento_code = models.CharField(max_length=3, null=True)
    punto_venta_code = models.CharField(max_length=3)
    secuencial = models.IntegerField(default=1)

    def __str__(self):
        return self.public_key