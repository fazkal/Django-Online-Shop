from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import AdminPasswordChangeForm,AdminProfileEditForm
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


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