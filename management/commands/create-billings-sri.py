import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import json

from anubisoft_billings.models import BusinessBilling
from configuration.location.models import *
from ecommerce_web.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Procesar Facturación electrónica'

    def handle(self, *args, **kwargs):
        public_key = input("public key: ")
        secret_key = input("secret key: ")
        establecimiento_code = input("Establecimiento code: ")
        punto_venta_code = input("Punto de venta code: ")
        BusinessBilling(
            public_key=public_key,
            secret_key=secret_key,
            establecimiento_code=establecimiento_code,
            punto_venta_code=punto_venta_code,
        ).save()
        print("KEYS CREATED SUCCESSFULLY")