from django.urls import path,include
from . import views 

app_name = 'website'

urlpatterns = [
    
    path('',views.IndexView.as_view(),name='index'),
    path('about/',views.AboutView.as_view(),name='about-us'),
    path('contact/',views.ContactView.as_view(),name='contact-us')
]
