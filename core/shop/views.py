from .models import ProductModel,ProductStatusType,ProductCategoryModel,WishlistProductModel
from django.views.generic import ListView,DetailView,View
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

# Create your views here.

class ShopProductListView(ListView):

    template_name = "shop/product-list.html"
    paginate_by = 5
    
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
        context['wishlist_items'] = WishlistProductModel.objects.filter(
                    user=self.request.user).values_list(
                    'product__id',flat=True)if self.request.user.is_authenticated else []
        return context
    

class ShopProductDetailView(DetailView):

    template_name = "shop/product-detail.html"
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_wished'] = WishlistProductModel.objects.filter(
                    user=self.request.user,product__id=
                    self.get_object().id).exists()if self.request.user.is_authenticated else False
        return context
    

class AddOrRemoveWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        message = ""
        added = False
        
        if not product_id:
            return JsonResponse({'message': 'شناسه محصول نامعتبر است', 'added': added}, status=400)
            
        try:
            product = ProductModel.objects.get(id=product_id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            return JsonResponse({'message': 'محصول یافت نشد', 'added': added}, status=404)
            
        try:
            wishlist_item = WishlistProductModel.objects.get(user=request.user, product=product)
            wishlist_item.delete()
            message = "محصول از لیست علایق حذف شد."
            added = False
        except WishlistProductModel.DoesNotExist:
            WishlistProductModel.objects.create(user=request.user, product=product)
            message = "محصول به لیست علایق اضافه شد."
            added = True
            
        return JsonResponse({'message': message, 'added': added})