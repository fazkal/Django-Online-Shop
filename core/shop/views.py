from .models import ProductModel,ProductStatusType,ProductCategoryModel
from django.views.generic import ListView,DetailView
from django.core.exceptions import FieldError

# Create your views here.

class ShopProductListView(ListView):

    template_name = "shop/product-list.html"
    paginate_by = 9
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size",self.paginate_by)

    def get_queryset(self):
        queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)
        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id:= self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price:= self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price:= self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by:= self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategoryModel.objects.all()
        return context
    

class ShopProductDetailView(DetailView):

    template_name = "shop/product-detail.html"
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)