from django.conf.urls import url
from django.urls import path

from . import views

app_name='blacklist'

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^search/$',views.search,name='search'),
    url(r'^move_version/$',views.move_version,name='move_version'),
    url(r'^add/$',views.add_new,name='add_new'),
]
