from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

from .models import Version, Blacks
from .forms import inputForm

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

def add_new(request):
    global version
    f=inputForm(request.POST)
    if f.is_valid():
        curr_ver = Version.objects.get(version_name=version)
        r_chr = request.POST['chr']
        r_pos = request.POST['pos']
        r_rsid = request.POST['rsid']
        r_reason = request.POST['reason']
        r_who = request.POST['who']
        c = curr_ver.blacks_set.create(chr=r_chr,pos=r_pos, rsid=r_rsid, reason=r_reason, who=r_who)
        return HttpResponseRedirect(reverse('blacklist:index'))
    else:
        print(f)
        messages.info(request, 'blank not allowed.. check the input data')
        return HttpResponseRedirect(reverse('blacklist:index'))
