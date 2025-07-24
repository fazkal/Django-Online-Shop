from order.permissions import HasCustomerAccessPermission
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class OrderCheckOutView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = 'order/checkout.html'