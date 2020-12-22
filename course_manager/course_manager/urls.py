"""course_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import views as project_views


##################################################################################################################

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', project_views.HomePage.as_view(), name='homepage'),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('courses/', include('courses.urls', namespace='courses')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += (
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler404 = 'course_manager.views.error_404_view'
handler500 = 'course_manager.views.error_500_view'
handler403 = 'course_manager.views.error_403_view'
handler400 = 'course_manager.views.error_400_view'


