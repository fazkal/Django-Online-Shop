from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import ProductModel,ProductStatusType,ProductCategoryModel

# Create your views here.

class ShopProductListView(ListView):

    template_name = "shop/product-list.html"
    paginate_by = 9
    
    def get_queryset(self):
        queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)
        if search_q:=self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id:=self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
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