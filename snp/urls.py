from django.conf.urls import url
from django.urls import path

from . import views

app_name='snp'

urlpatterns=[
    url(r'^$',views.main,name='main'),
    url(r'^file_download/$', views.file_download, name='file_download'),
    url(r'^file_report/$', views.file_report, name='file_report'),
    url(r'^one_report/$', views.one_report, name='one_report'),
    url(r'^usage/$', views.usage, name='usage'),

]
