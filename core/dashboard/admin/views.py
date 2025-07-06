from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AdminDashboardHomeView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/admin/home.html'