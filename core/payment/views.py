
from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType

class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(
            PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        
        
        if status == "OK":
            zarin_pal = ZarinPalSandbox() 
            response = zarin_pal.payment_verify(
                int(payment_obj.amount), payment_obj.authority_id)
            
            
            if 'data' in response and 'ref_id' in response['data']:
                ref_id = response["data"]["ref_id"]
                status_code = response["data"]["code"]

                payment_obj.ref_id = ref_id
                payment_obj.response_code = status_code
                payment_obj.status = PaymentStatusType.success.value if status_code in {
                    100, 101} else PaymentStatusType.failed.value
                payment_obj.response_json = response
                payment_obj.save()

                order.status = OrderStatusType.success.value if status_code in {
                    100, 101} else OrderStatusType.failed.value
                order.save()

                return redirect(reverse_lazy("order:completed") if status_code in {100, 101} else reverse_lazy("order:failed"))
            else:
                
                payment_obj.status = PaymentStatusType.failed.value
                payment_obj.response_json = response
                payment_obj.save()
                order.status = OrderStatusType.failed.value
                order.save()
                return redirect(reverse_lazy("order:failed"))
        else:
            
            payment_obj.status = PaymentStatusType.failed.value  
            payment_obj.response_json = {"Status": status, "Message": "Payment cancelled by user or failed."}
            payment_obj.save()
            order.status = OrderStatusType.failed.value
            order.save()
            return redirect(reverse_lazy("order:failed"))

