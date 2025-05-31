from django.urls import path,include
from . import views 

app_name = 'shop'

urlpatterns = [
    
    path('product/list/',views.ShopProductListView.as_view(),name='product-list'),
    path(r"product/(?P<slug>[-\w]+)/detail/",views.ShopProductDetailView.as_view(),name="product-detail")
    
]
