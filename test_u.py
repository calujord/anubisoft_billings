import unittest

from anubisoft_billings.billing_sri import SRIBillings
from anubisoft_ecommerce.orders.models import Order


class MyTestCase(unittest.TestCase):
    def test_something(self):
        order = Order.objects.get(pk=8)
        sri_billings = SRIBillings(order=order)
        url_pdf = sri_billings.send()
        print(url_pdf)


if __name__ == '__main__':
    unittest.main()
