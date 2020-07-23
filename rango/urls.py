from django.conf.urls import url
from rango import views


urlpatterns = [
    url(r'^$', views.index, name= 'index'),
    url(r'^about', views.about, name= 'about'),
    url(r'^add_category/$', views.add_catagory, name='add_category'),
    url(r'catagory/(?P<catagory_name_slug>[\w\-]+)/$',views.show_catagory, name='show_category'),
    url(r'^catagory/(?P<catagory_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]
