#! /usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = 'CARLOS JORDAN'

import requests

from anubisoft_billings.serializer.anubisoft_billings import AnubisoftBillingsSerializer
from anubisoft_ecommerce.orders.models import Order

from datetime import datetime
import hashlib
import os
from django.utils.encoding import smart_str
from django.db.models import Count
from django.conf import settings
import json

import base64

AS_BILLINGS_URL = "http://www.tu-efactura.ec:8080"


class SRIBillings:
    order: Order = None

    def __init__(self, order: Order = None):
        self.order = order

    def send(self):
        if self.order.pending_to_billing:
            url = "%s/receptorComprobantesNeutros/rest/factura" % (AS_BILLINGS_URL)
            data = json.dumps(self.order, cls=AnubisoftBillingsSerializer, indent=4)
            headers = {'Content-Type': 'application/json'}
            response = requests.request(
                "POST", url,
                data=data, headers=headers
            )
            print(response)
            if response != "":
                data_received = json.loads(response.text)
                url_pdf = "https://www.tu-efactura.ec/visorRideXml/VisorRide?claveAcceso=%s" % data_received.get(
                    "claveAcceso")
                self.order.pending_to_billing = False
                self.order.url_billing = url_pdf
                self.order.save()
                return url_pdf
        return None
