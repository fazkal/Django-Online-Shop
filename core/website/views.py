from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):

    template_name = "website/index.html"


class AboutView(TemplateView):

    template_name = 'website/about-us.html'


class ContactView(TemplateView):

    template_name = 'website/contact-us.html'