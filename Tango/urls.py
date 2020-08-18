"""Tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from registration.backends.simple.urls import RegistrationView
from rango import views

class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return reverse('register_profile')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rango/', include('rango.urls')),
    #above maps any urls starting with rango
    #to be handles by the rango app
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$',MyRegistrationView.as_view(),name= 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^password/', include('registration.backends.simple.urls')),
    url(r'^profiles/$', views.list_profiles, name= 'list_profiles'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


