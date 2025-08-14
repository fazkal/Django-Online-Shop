from django.urls import path,include
from . import views 

app_name = 'customer'

urlpatterns = [

    path('home/',views.CustomerDashboardHomeView.as_view(),name='home'),
    path('security-edit/',views.SecurityEditView.as_view(),name='security-edit'),
    path('profile-edit/',views.CustomerProfileEditView.as_view(),name='profile-edit'),
    path('profile-image-edit/',views.CustomerProfileImagEditView.as_view(),name='profile-image-edit'),

    path('address/list/',views.CustomerAddressListView.as_view(),name='address-list'),
    path('address/create/',views.CustomerAddressCreateView.as_view(),name='address-create'),
    path('address/<int:pk>/edit/',views.CustomerAddressEditView.as_view(),name='address-edit'),
    path('address/<int:pk>/delete/',views.CustomerAddressDeleteView.as_view(),name='address-delete'),

    path('order/list/',views.CustomerOrderListView.as_view(),name='order-list'),
    path('order/<int:pk>/detail/',views.CustomerOrderDetailView.as_view(),name='order-detail'),

    path('wishlist/list/',views.CustomerWishlistListView.as_view(),name='wishlist-list'),
    path('wishlist/<int:pk>/delete/',views.WishlistDeleteView.as_view(),name='wishlist-delete')

]