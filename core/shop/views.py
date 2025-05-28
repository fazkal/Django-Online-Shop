from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ShopProductListView(TemplateView):

    template_name = "shop/product-list.html"