from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import generic
from .models import tbValues
from django.contrib import messages
import pandas as pd
from io import StringIO
from .forms import inputForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os

search_dic = {'option_name': '', 'search_keyword':''}

def main(request):
    return render(request,'infos/home.html')

def index(request):
    global search_dic
    # if there is an exist search keyword, show search result page
    if search_dic['search_keyword'] != '':
        return HttpResponseRedirect(reverse('infos:search'))
    else:
        tbValues_list=tbValues.objects.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(tbValues_list, 20)
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
                
        context={'tbValues_list':result}

    return render(request,'infos/index.html',context)


#detail page is for modify(edit data/ remove data)
def detail(request, id):

    tb = tbValues.objects.get(pk=id)
    context = {'result': tb }
    return render(request, 'infos/detail.html',context)


def edit_done(request,id):
    original=get_object_or_404(tbValues, pk=id)
    f=inputForm(request.POST)
    if f.is_valid():

        original.rack_num=request.POST['rack_num']
        original.box_num=request.POST['box_num']
        original.barcode_num=request.POST['barcode_num']
        original.well_num=request.POST['well_num']
        original.freezer_num=request.POST['freezer_num']
        original.save()
        messages.info(request, 'edit done ! ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'blank not allowed... check the edit data')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#get id from the html, and delete from database
def remove(request,id):
    tbvalue=tbValues.objects.get(pk=id)
    tbvalue.delete()
    messages.info(request, 'delete done')
    return HttpResponseRedirect(reverse('infos:index'))


#add new data
def add_new(request):
    f=inputForm(request.POST)
    if f.is_valid():
        tb=tbValues(rack_num=request.POST['rack_num'],box_num=request.POST['box_num'],barcode_num=request.POST['barcode_num'],well_num=request.POST['well_num'],freezer_num=request.POST['freezer_num'])
        tb.save()
        return HttpResponseRedirect(reverse('infos:index'))
    else:
        messages.info(request, 'blank not allowed.. check the input data')
        return HttpResponseRedirect(reverse('infos:index'))



# -----------------------------
# search 
# -----------------------------
def search_btn(request):
    #this function called when user clicked search button
    global search_dic
    search_dic['option_name'] = request.POST['option_name']
    search_dic['search_keyword'] = request.POST['search']

    return HttpResponseRedirect(reverse('infos:search'))


#search data with entered keyword
def search(request):
    global search_dic

    #get keyword -> make list with result objects
    # if keyword is null, show full list
    if search_dic['search_keyword'] == '':
        return HttpResponseRedirect(reverse('infos:index'))

    else:
        search_list = search_result()

        result="results '"+search_dic['search_keyword'] + "' in "+ search_dic['option_name']

        page = request.GET.get('page',1)
        paginator = Paginator(search_list, 10)
        try:
            value = paginator.page(page)
        except PageNotAnInteger:
            value = paginator.page(1)
        except EmptyPage:
            value = paginator.page(paginator.num_pages)


        context={'tbValues_list': value, 'result':result}

    return render(request, 'infos/index.html', context)


#each option name (html->combobox data) have different filter parameter
def search_result():
    global search_dic
    option_name = search_dic['option_name']
    search_keyword = search_dic['search_keyword']

    if option_name == 'barcode_num':
        return tbValues.objects.filter(barcode_num__contains=search_keyword)
    elif option_name == 'freezer_num':
        return tbValues.objects.filter(freezer_num__contains=search_keyword)
    elif option_name == 'box_num':
        return tbValues.objects.filter(box_num__contains=search_keyword)
    elif option_name == 'rack_num':
        return tbValues.objects.filter(rack_num__contains=search_keyword)
    elif option_name == 'well_num':
        return tbValues.objects.filter(well_num__contains=search_keyword)



#----------------------------------------------------
# file upload and download example

#open and read file -> insert data in to database
def upload(request):
    try:
        if request.FILES.__len__()==0:
            messages.info(request, 'There are no files !')
            return HttpResponseRedirect(reverse('infos:index'))

        uploadfile = request.FILES['file']
        if uploadfile.name.find('csv')<0:
            messages.info(request, ' This is not csv file !')
            return HttpResponseRedirect(reverse('infos:index'))

        read=uploadfile.read().decode('utf8')
        testdata=StringIO(read)
        data=pd.read_csv(testdata, sep='\t')
        #print(data)

        #check the null data in txt file
        if data.isnull().sum().sum()!=0:
            print(data)
            messages.info(request, 'check the file ! null data in file ')
            return HttpResponseRedirect(reverse('infos:index'))
        #else, data save
        else:
            for index,row in data.iterrows():
                tb=tbValues(rack_num=row['rack_num'],box_num=row['box_num'],barcode_num=row['barcode_num'],well_num=row['well_num'],freezer_num=row['freezer_num'])
                print(tb)
                tb.save()
            messages.info(request, 'upload done !')
            return HttpResponseRedirect(reverse('infos:index'))
    except Exception as e:
        print(e)
        messages.info(request, 'check the file ! [ '+ str(e) + ']')
        return HttpResponseRedirect(reverse('infos:index'))

def file_download(request):
    f=str(os.getcwd())+'/examples/example_infos.csv'
    response = HttpResponse(open(f,'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(inventory).csv"'
    return response



#--------------------------------------

def usage(request):
    return render(request, 'infos/usage.html')


# -------------------------
# download current table on the web page
def download_all(request):
    global search_dic

    if search_dic['search_keyword'] != '':
        search_list = search_result()
        srh="results '" + search_dic['search_keyword'] + "' in "+ search_dic['option_name']

        context = { 'result':search_list, 'srh':srh}

    else:
        search_list = tbValues.objects.all()
        context = { 'result':search_list}

    return render(request, 'infos/download_all.html', context)


def drop_table(request):
    global search_dic
    pwd = request.POST['password']
    if pwd == 'inspiron':
        tbValues.objects.all().delete()
        print('--------------------------------- clear data ---------------------------------')
        search_dic['option_name']=''
        search_dic['search_keyword']=''

        return HttpResponseRedirect(reverse('infos:index'))
    else:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
