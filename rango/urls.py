from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name= 'index'),
    url(r'^about', views.about, name= 'about'),
    url(r'catagory/(?P<catagory_name_slug>[\w\-]+)/$',
        views.show_catagory, name='show_category'),
]
