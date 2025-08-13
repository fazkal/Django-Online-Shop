from django.urls import path,include
from . import views 

app_name = 'admin'

urlpatterns = [

    path('home/',views.AdminDashboardHomeView.as_view(),name='home'),
    path('security-edit/',views.SecurityEditView.as_view(),name='security-edit'),
    path('profile-edit/',views.AdminProfileEditView.as_view(),name='profile-edit'),
    path('profile-image-edit/',views.AdminProfileImagEditView.as_view(),name='profile-image-edit'),
    path('product/list/',views.AdminProductsListView.as_view(),name='product-list'),
    path('product/<int:pk>/edit/',views.AdminProductsEditView.as_view(),name='product-edit'),
    path('product/<int:pk>/delete/',views.AdminProductsDeleteView.as_view(),name='product-delete'),
    path('product/create/',views.AdminProductsCreateView.as_view(),name='product-create'),
    path("order/list/",views.AdminOrderListView.as_view(),name="order-list"),
    path("order/<int:pk>/detail/",views.AdminOrderDetailView.as_view(),name="order-detail")
    
]