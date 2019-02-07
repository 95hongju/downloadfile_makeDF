from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Version, Blacks

version = 'GSAv1.2'


def index(request):
    global version
    curr_ver = Version.objects.get(version_name=version)
    blacks = curr_ver.blacks_set.all()
    context = {'version': version, 'result':blacks}
    return render(request, 'blacklist/index.html', context)


def move_version(request):
    global version
    des_ver = request.POST['version_name']
    version = des_ver
    return HttpResponseRedirect(reverse('blacklist:index'))


def search(request):
    return HttpResponse('search')
