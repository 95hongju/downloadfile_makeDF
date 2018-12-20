from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^update/$', views.update, name='update'),
    url(r'^searchRS/$', views.searchRS, name='searchRS'),
    url(r'^file_download/$', views.file_download, name='file_download'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/result_download/$', views.result_download, name='result_download'),
]
