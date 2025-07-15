from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import CustomerPasswordChangeForm,CustomerProfileEditForm
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


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