from django.conf.urls import url
from django.urls import path

from . import views

app_name='blacklist'

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^search/$',views.search,name='search'),
    url(r'^move_version/$',views.move_version,name='move_version'),
    url(r'^add/$',views.add_new,name='add_new'),
    url(r'^(?P<id>[0-9]+)/remove/$',views.remove,name='remove'),
    url(r'^(?P<id>[0-9]+)/edit/$',views.edit,name='edit'),
    url(r'^(?P<id>[0-9]+)/edit_done/$',views.edit_done,name='edit_done'),
    url(r'^file_download/$',views.file_download,name='file_download'),
    url(r'^upload/$',views.upload,name='upload'),
    url(r'^usage/$',views.usage,name='usage'),
]
