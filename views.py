from django.views.generic import FormView, TemplateView, ListView

from anubisoft_ecommerce.orders.models import Order


class SendSRIFormView(ListView):
    template_name = "billings/order-pending.html"

    def get_queryset(self):
        return Order.objects.filter(
            # pending_to_billing=True,
            is_finished=True
        ).exclude(
            ordertracking__status__name="REJECT"
        ).order_by("-pk")
