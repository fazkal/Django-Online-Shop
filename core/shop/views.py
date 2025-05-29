from django.shortcuts import render
from django.views.generic import ListView
from .models import ProductModel,ProductStatusType

# Create your views here.

class ShopProductListView(ListView):

    template_name = "shop/product-list.html"
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)