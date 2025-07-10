from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name = 'dashboard/admin/home.html'


class SecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,
                       SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('dashboard:admin:security-edit')
    success_message = "بروزرسانی رمز با موفقیت انجام شد"

