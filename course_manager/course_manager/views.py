from django.views import generic
from django.shortcuts import render
from django.conf import settings

##################################################################################################################


class HomePage(generic.TemplateView):
    template_name = 'index.html'





