from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^searchRS/$', views.searchRS, name='searchRS'),
    url(r'^file_downloadRS/$', views.file_downloadRS, name='file_downloadRS'),
    url(r'^uploadRS/$', views.uploadRS, name='uploadRS'),

    url(r'^searchPC/$', views.searchPC, name='searchPC'),
    url(r'^file_downloadPC/$', views.file_downloadPC, name='file_downloadPC'),
    url(r'^uploadPC/$', views.uploadPC, name='uploadPC'),
    url(r'^usage/$', views.usage, name='usage'),
]
