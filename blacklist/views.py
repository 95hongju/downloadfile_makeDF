from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from io import StringIO
import pandas as pd
import os

from .models import Version, Blacks
from .forms import inputForm


#default version
version = 'GSAv1.2'


def index(request):
    global version
    curr_ver = Version.objects.get(version_name=version)
    blacks = curr_ver.blacks_set.all()
    context = {'version': version, 'result':blacks}
    return render(request, 'blacklist/index.html', context)


# ---------------------------------------
# change version
# ---------------------------------------
def move_version(request):
    global version
    des_ver = request.POST['version_name']
    version = des_ver
    return HttpResponseRedirect(reverse('blacklist:index'))


# ---------------------------------------
# add new data into database
# ---------------------------------------
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


# ---------------------------------------
# database remove
# ---------------------------------------
def remove(request, id):
    blk = Blacks.objects.get(pk=id)
    blk.delete()
    messages.info(request, 'delete done')
    return HttpResponseRedirect(reverse('blacklist:index'))


# ---------------------------------------
# database edit
# ---------------------------------------
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


# ---------------------------------------
# search data in database
# ---------------------------------------
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


# ---------------------------------------
# file upload & download
# ---------------------------------------

#example file download
def file_download(request):
    f=str(os.getcwd())+'/examples/example_blacklist.csv'
    response = HttpResponse(open(f,'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(blacklist).csv"'
    return response


#open and read file -> insert data in to database
def upload(request):
    global version

    try:
        #no file
        if request.FILES.__len__()==0:
            messages.info(request, 'There are no files !')
            return HttpResponseRedirect(reverse('blacklist:index'))
        #not csv file
        uploadfile = request.FILES['file']
        if uploadfile.name.find('csv')<0:
            messages.info(request, ' This is not csv file !')
            return HttpResponseRedirect(reverse('blacklist:index'))

        #read file
        read = uploadfile.read().decode('utf8')
        testdata = StringIO(read)
        dtypes = {'CHR':str, 'POS':str, 'rsID':str,'Reason':str, 'Registered by':str}
        data = pd.read_csv(testdata, sep='\t', dtype = dtypes)

        #allow null only in rsID
        data['rsID'] = data['rsID'].fillna('N/A')

        #check the null data in txt file
        if data.isnull().sum().sum()!=0:
            print(data)
            messages.info(request, 'check the file ! null data in file (blank only allowed in rsID) ')
            return HttpResponseRedirect(reverse('blacklist:index'))

        #else, data save
        else:
            q = Version.objects.get(version_name=version)

            for index, row in data.iterrows():
                c = q.blacks_set.create(chr=row['CHR'],pos=row['POS'],rsid=row['rsID'],reason=row['Reason'],who=row['Registered by'])

            messages.info(request, 'upload & save done !')
            return HttpResponseRedirect(reverse('blacklist:index'))

    except Exception as e:
        print(e)
        messages.info(request, 'check the file ! [ '+ str(e) + ']')
        return HttpResponseRedirect(reverse('blacklist:index'))


def usage(request):
    return render(request, 'blacklist/usage.html')
