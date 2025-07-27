from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import CustomerPasswordChangeForm,CustomerProfileEditForm,UserAddressForm
from accounts.models import Profile
from order.models import UserAddressModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import FieldError


class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = 'dashboard/customer/home.html'


class SecurityEditView(LoginRequiredMixin,HasCustomerAccessPermission,
                       SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name = 'dashboard/customer/profile/security-edit.html'
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy('dashboard:customer:security-edit')
    success_message = "بروزرسانی رمز با موفقیت انجام شد"


class CustomerProfileEditView (LoginRequiredMixin,HasCustomerAccessPermission,
                       SuccessMessageMixin,UpdateView):
    template_name = 'dashboard/customer/profile/profile-edit.html'
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    

class CustomerProfileImagEditView(LoginRequiredMixin,HasCustomerAccessPermission,
                       SuccessMessageMixin,UpdateView):
    http_method_names = ['post']
    model = Profile
    fields = ['image']
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = 'بروزرسانی تصویر پروفایل با موفقیت انجام شد'

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request,'ارسال تصویر با مشکل مواجه شد لطفا مجددا تلاش نمایید')
        return redirect(self.success_url)
    

class CustomerAddressListView(LoginRequiredMixin,HasCustomerAccessPermission,ListView):
    template_name = 'dashboard/customer/addresses/address-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',self.paginate_by)
    
    def get_queryset(self):
        queryset = UserAddressModel.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get('q'):
            queryset = queryset.filter(address__icontains=search_q)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.filter(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context


class CustomerAddressCreateView(LoginRequiredMixin,HasCustomerAccessPermission,
                                SuccessMessageMixin,CreateView):
    template_name = 'dashboard/customer/addresses/address-create.html'

    form_class = UserAddressForm
    success_message = 'ایجاد آدرس با موفقیت انجام شد'

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy('dashboard:customer:address-edit',kwargs={'pk':form.instance.pk}))
    
    def get_success_url(self):
        return reverse_lazy('dashboard:customer:address-list')
    

class CustomerAddressEditView(LoginRequiredMixin,HasCustomerAccessPermission,
                              SuccessMessageMixin,UpdateView):
    template_name = 'dashboard/customer/addresses/address-edit.html'
    form_class = UserAddressForm
    success_message = 'ویرایش آدرس با موفقیت انجام شد'

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('dashboard:customer:address-edit',kwargs={'pk':self.get_object().pk})
    

class CustomerAddressDeleteView(LoginRequiredMixin,HasCustomerAccessPermission,
                                SuccessMessageMixin,DeleteView):
    template_name = 'dashboard/customer/addresses/address-delete.html'
    success_url = reverse_lazy('dashboard:customer:address-list')
    success_message = 'حذف آدرس با موفقیت انجام شد'

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)