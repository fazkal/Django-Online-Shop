from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import AdminPasswordChangeForm,AdminProfileEditForm
from accounts.models import Profile
from shop.models import ProductModel,ProductStatusType,ProductCategoryModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView,UpdateView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import FieldError


class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name = 'dashboard/admin/home.html'


class SecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,
                       SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('dashboard:admin:security-edit')
    success_message = "بروزرسانی رمز با موفقیت انجام شد"


class AdminProfileEditView(LoginRequiredMixin,HasAdminAccessPermission,
                       SuccessMessageMixin,UpdateView):
    template_name = 'dashboard/admin/profile/profile-edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    

class AdminProfileImagEditView(LoginRequiredMixin,HasAdminAccessPermission,
                       SuccessMessageMixin,UpdateView):
    http_method_names = ['post']
    model = Profile
    fields = ['image']
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = 'بروزرسانی تصویر پروفایل با موفقیت انجام شد'

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request,'ارسال تصویر با مشکل مواجه شد لطفا مجددا تلاش نمایید')
        return redirect(self.success_url)
    

class AdminProductsListView(LoginRequiredMixin,HasAdminAccessPermission,
                            ListView):
    template_name = "dashboard/admin/products/product-list.html"
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size",self.paginate_by)

    def get_queryset(self):
        queryset = ProductModel.objects.all()
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