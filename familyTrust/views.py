from django.shortcuts import render
from django.views.generic import TemplateView

class Trust(TemplateView):
    template_name = 'familyTrust/trust.html'