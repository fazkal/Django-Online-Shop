from django.urls import path,include
from . import views 

app_name = 'admin'

urlpatterns = [

    path('home/',views.AdminDashboardHomeView.as_view(),name='home'),
    path('security-edit/',views.SecurityEditView.as_view(),name='security-edit'),
    path('profile-edit/',views.AdminProfileEditView.as_view(),name='profile-edit'),
    path('profile-image-edit/',views.AdminProfileImagEditView.as_view(),name='profile-image-edit'),
    path('product/list/',views.AdminProductsListView.as_view(),name='product-list')
    
]