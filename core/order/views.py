from order.permissions import HasCustomerAccessPermission
from order.models import UserAddressModel
from .forms import CheckOutForm
from cart.models import CartModel
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class OrderCheckOutView(LoginRequiredMixin,HasCustomerAccessPermission,FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        context['addresses'] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context['total_price'] = total_price
        context['total_tax'] = round((total_price * 9) / 100)
        return context