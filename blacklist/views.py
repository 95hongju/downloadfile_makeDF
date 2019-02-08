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
        if(r_rsid ==''):
            r_rsid='N/A'
        c = curr_ver.blacks_set.create(chr=r_chr,pos=r_pos, rsid=r_rsid, reason=r_reason, who=r_who)
        return HttpResponseRedirect(reverse('blacklist:index'))
    else:
        print(f)
        messages.info(request, 'blank not allowed.. check the input data')
        return HttpResponseRedirect(reverse('blacklist:index'))


def remove(request, id):
    blk = Blacks.objects.get(pk=id)
    blk.delete()
    messages.info(request, 'delete done')
    return HttpResponseRedirect(reverse('blacklist:index'))


def edit(request,id):
    try:
        global version
        blk = Blacks.objects.get(pk=id)
        q = Version.objects.get(version_name=version)
        blk_list = q.blacks_set.all()
        context ={'blk_list':blk_list,'blk':blk,'version':version}
        return render(request,'blacklist/edit.html',context)
    except:
        messages.info(request, 'error : invalid pkID')
        return HttpResponseRedirect(reverse('blacklist:index'))


def edit_done(request,id):
    try:
        blk = Blacks.objects.get(pk=id)
        f=inputForm(request.POST)
        if f.is_valid():
            if request.POST['rsid']== '':
                blk.rsid='N/A'
            else:
                blk.rsid = request.POST['rsid']
            blk.chr = request.POST['chr']
            blk.pos = request.POST['pos']
            blk.reason = request.POST['reason']
            blk.who = request.POST['who']

            blk.save()
            messages.info(request, 'edit done ! ')
            return HttpResponseRedirect(reverse('blacklist:index'))
        else:
            print(request.POST)
            print("error")
            messages.info(request, 'blank not allowed(except rsID)... check the edit data')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.info(request, 'error : invalid pkID')
        return HttpResponseRedirect(reverse('blacklist:index'))


def search(request):
    global version
    #select box value
    option_name=request.POST['option_name']
    search_keyword=request.POST['searchword']
    #get keyword -> make list with result objects
    if search_keyword=='':
        q = Version.objects.get(version_name= version)
        c = q.blacks_set.all()
        context={'version':version, 'result' : c}
    else:
        blk_list=search_result(option_name, search_keyword, version)
        srh="results '"+search_keyword + "' in "+option_name+'('+version+')'
        context={'result': blk_list,'srh':srh, 'version':version}
    return render(request,'blacklist/index.html',context)


#each option name (html->combobox data) have different filter parameter
def search_result(option_name, search_keyword,version):
    q = Version.objects.get(version_name=version)

    if option_name == 'CHR':
        return q.blacks_set.filter(chr__contains=search_keyword)
    elif option_name == 'POS':
        return q.blacks_set.filter(pos__contains=search_keyword)
    elif option_name == 'rsID':
        return q.blacks_set.filter(rsid__contains=search_keyword)
    elif option_name == 'WHO':
        return q.blacks_set.filter(who__contains=search_keyword)
