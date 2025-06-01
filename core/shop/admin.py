from django.contrib import admin
from .models import ProductCategoryModel,ProductImageModel,ProductModel

# Register your models here.

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title','price','discount_percent','stock','status','created_date')


@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title','created_date')


@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ('product','created_date')

    def product_title(self, obj):
        return obj.product.title

    product_title.short_description = 'Product Title' 