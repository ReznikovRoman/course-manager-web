from django.views import generic
from django.shortcuts import render
from django.conf import settings

##################################################################################################################


class HomePage(generic.TemplateView):
    template_name = 'index.html'


############################################################################################################


def error_404_view(request, *args, **kwargs):
    response = render(request, '404_page.html')
    response.status_code = 404
    return response


def error_500_view(request, *args, **kwargs):
    response = render(request, '500_page.html')
    response.status_code = 500
    return response


def error_403_view(request, *args, **kwargs):
    response = render(request, '403_page.html')
    response.status_code = 403
    return response


def error_400_view(request, *args, **kwargs):
    response = render(request, '400_page.html')
    response.status_code = 400
    return response





