from anubisoft_billings.models import BusinessBilling
from anubisoft_ecommerce.orders.models import Order, OrderDetail, BillingSRI
from django.utils.translation import gettext_lazy as _

from api_rest.utils.encode import APIJsonEncode


class AnubisoftBillingsSerializer(APIJsonEncode):
    def default(self, o):
        if isinstance(o, Order):
            business_billing: BusinessBilling = BusinessBilling.objects.all().last()
            if business_billing is None:
                raise Exception("FACTURACIÓN ELECTRÓNICA NO CONFIGURADA")
            order_detail_list = list(o.get_order_detail())
            if o.address:
                order_detail_list.append(BillingSRI(total=o.get_total_delivery(), description=str(_("delivery")).capitalize()))

            data = dict(
                rucEmisor=business_billing.public_key, #"U60zUbgoI+q6b6v3IO5D8Q==",
                tokenSeguro=business_billing.secret_key, #"wH8xajECFFk=",
                codigoEstablecimiento=business_billing.establecimiento_code, # "001",
                codigoPuntoVenta=business_billing.punto_venta_code, #"003",
                tipoIdentificacionCliente="04" if len(o.billing.identification) == 13 else "05" if len(
                    o.billing.identification) == 10 else "06",
                razonSocialCliente=o.billing.name,
                nota1="Orden No. %s" % o.pk,
                nota2="Ciudad: %s %s" % (o.address.canton.nombre, o.address.canton.provincia.nombre) if o.address is not None and o.address.canton is not None else 'No definida',
                nota3="Teléfono: %s" % o.address.phone if o.address is not None else 'No definido',
                nota4="Nombre de contacto: %s %s" % (o.address.first_name, o.address.last_name) if o.address is not None else 'No definido',
                nota5="Categoría: %s" % order_detail_list[0].product.get_categories()[0] if len(order_detail_list) > 0 and len(order_detail_list[0].product.get_categories()) > 0 else '',
                esElectronico=True, codigoSucursalCliente=None,
                identificacionCliente=o.billing.identification,
                correoElectronicoCliente=o.billing.email,
                direccionCliente=o.billing.address_name,
                detalles=order_detail_list,
                pagos=[
                    dict(formaPago=o.get_code_payment(), monto=o.get_total()) # preguntar las formas de pago
                ]
            )
            if o.billing_number is not None:
                data["secuenciaDocumento"] = '%09d' % o.billing_number
            return data
        elif isinstance(o, BillingSRI):
            return dict(
                codigo="DELIVERY",
                descripcion=o.description,
                nota=None,
                cantidad=o.quantity,
                precioUnitario=o.total,
                descuento=0.0,
                ice=0,
                iva=o.get_taxes(),
                total=o.get_total_service_price(),
                codigoIVA="2" if o.get_taxes() > 0 else "0",
                fechaExpiracion=None, lote=None, serie=None, producto=True
            )
        elif isinstance(o, OrderDetail):
            return dict(
                codigo=o.product.internal_code,
                descripcion=o.product.name,
                nota=o.product.description,
                cantidad=o.quantity,
                precioUnitario=o.get_service_price_without_taxes(),
                descuento=o.get_discount_product_value(),
                ice=0,
                iva=o.get_taxes(),
                total=o.get_total_service_price(),
                codigoIVA="2" if o.get_taxes() > 0 else "0",
                fechaExpiracion=None, lote=None, serie=None, producto=True
            )

