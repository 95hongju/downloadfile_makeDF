"""download_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from infos import views
from django.contrib.auth.models import User,Group

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),
    path('infos/', include('infos.urls')),
    path('snp/', include('snp.urls')),
    path('blacklist/', include('blacklist.urls')),
]

admin.site.site_header = "Diagnomics Admin"
admin.site.site_title = "Diagnomics Admin Portal"
admin.site.index_title = "Welcome to Diagnomics Admin Portal"

admin.site.unregister(User)
admin.site.unregister(Group)
