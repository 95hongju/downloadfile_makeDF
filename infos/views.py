from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import generic
from .models import tbValues
from django.contrib import messages
import pandas as pd
from io import StringIO
from .forms import inputForm
import os


def index(request):
    tbValues_list=tbValues.objects.all()
    context={'tbValues_list':tbValues_list}
    return render(request,'infos/index.html',context)

def edit(request,id):
    tbvalue=get_object_or_404(tbValues,pk=id)
    tbValues_list=tbValues.objects.all()
    return render(request,'infos/edit.html',{'tbValues_list':tbValues_list,'tbvalue':tbvalue})

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
        return HttpResponseRedirect(reverse('infos:index'))
    else:
        print(request.POST)
        print("error")
        messages.info(request, 'blank not allowed... check the edit data')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#get id from the html, and delete from database

def remove(request,id):
    tbvalue=tbValues.objects.get(pk=id)
    tbvalue.delete()
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

#search data with entered keyword
def search(request):
    option_name=request.POST['option_name']
    search_keyword=request.POST['search']
    tbValues_list=search_result(option_name,search_keyword)
    if search_keyword=='':
        context={'tbValues_list': tbValues_list}
    else:
        result="results '"+search_keyword + "' in "+option_name
        context={'tbValues_list': tbValues_list,'result':result}
    return render(request,'infos/index.html',context)

#each option name (html->combobox data) have different filter parameter
def search_result(option_name, search_keyword):
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

#open and read file -> insert data in to database
def upload(request):
    try:
        if request.FILES.__len__()==0:
            messages.info(request, 'There are no files !')
            return HttpResponseRedirect(reverse('infos:index'))

        uploadfile = request.FILES['file']
        if uploadfile.name.find('txt')<0:
            messages.info(request, ' This is not txt file !')
            return HttpResponseRedirect(reverse('infos:index'))
        #read='rack_num\tbox_num\tbarcode_num\twell_num\tfreezer_num\n'
        #read+=uploadfile.read().decode('utf8')
        read=uploadfile.read().decode('utf8')

        testdata=StringIO(read)
        data=pd.read_csv(testdata,sep='\t')
        print(data)

        #check the null data in txt file
        if data.isnull().sum().sum()!=0:
            print(data)
            messages.info(request, 'check the file ! null data in file ')
            return HttpResponseRedirect(reverse('infos:index'))
        #else, data save
        else:
            for index,row in data.iterrows():
                tb=tbValues(rack_num=row['rack_num'],box_num=row['box_num'],barcode_num=row['barcode_num'],well_num=row['well_num'],freezer_num=row['freezer_num'])
                tb.save()
            messages.info(request, 'upload done !')
            return HttpResponseRedirect(reverse('infos:index'))
    except Exception as e:
        print(e)
        messages.info(request, 'check the file ! [ '+ str(e) + ']')
        return HttpResponseRedirect(reverse('infos:index'))

def file_download(request):
    f=str(os.getcwd())+'/examples/example_infos1.txt'
    response = HttpResponse(open(f,'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(barcode).txt"'
    return response
