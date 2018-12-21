from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import downloadFileList
from collections import OrderedDict
from io import StringIO
import pandas as pd
import os

import search.fileDownOpen as fd

columns = ['CHR', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'rsID', 'clinvar Annotation']
readfile = pd.DataFrame(columns=columns)
print(readfile.empty)

# Create your views here.
def main(request):
    global readfile

    # check the name from the urls
    fileOnURL=fd.find_date()
    print('-----> ',fileOnURL)

    # get queryset
    q = downloadFileList.objects.all()

    # if empty queryset, download file from url
    if len(q) == 0:
        filename = fileOnURL+'.vcf.gz'
        fd.down_process(filename)
        newone=downloadFileList(file_name=fileOnURL)
        newone.save()
    usingfile = downloadFileList.objects.latest('down_date')
    if readfile.empty:
        read_file_from_csv()


    context = {'currUsingFile': usingfile}
    return render(request, 'search/index.html', context)


def read_file_from_csv():
    global readfile

    usingfile = downloadFileList.objects.latest('down_date')
    print('read dataframe....')
    path = os.path.join(os.path.dirname(__file__))+'/data/'+usingfile.file_name+'.csv'
    dtypes = {'CHR': str, 'POS': str, 'ID': str, 'REF': str, 'ALT': str, 'QUAL': str, 'FILTER': str, 'rsID': str, 'clinvar Annotation': str}
    readfile = pd.read_csv(path, delimiter='\t', dtype=dtypes)


def update(request):

    fileOnURL=fd.find_date()
    currfile = downloadFileList.objects.latest('down_date')
    if currfile.file_name==fileOnURL:
        messages.info(request, '😎 already updated 😎')
        return HttpResponseRedirect(reverse('search:main'))
    else:
        filename = fileOnURL+'.vcf.gz'
        fd.down_process(filename)
        newone=downloadFileList(file_name=fileOnURL)
        newone.save()
        messages.info(request, '😁 update done 😁')
        return HttpResponseRedirect(reverse('search:main'))


def searchRS(request):
    global readfile
    if readfile.empty:
        read_file_from_csv()

    keyword = request.POST['srchkeyword']
    if 'RS' in keyword or 'rs' in keyword:
        if 'RS' in keyword:
            keyword = 'rs'+keyword.split('RS')[1]
        result = readfile.loc[readfile['rsID'] == keyword]
        if result.empty:
            messages.info(request, '😔 nothing to show 😔')
            return HttpResponseRedirect(reverse('search:main'))
        else:
            columnlist = ['rsID', 'CHR', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation']
            result = result[columnlist]
            result = result.fillna('N/A')
            dic = result.to_dict('records', into = OrderedDict)
            context = {'result': dic}
            return render(request, 'search/result.html', context)
    else:
        messages.info(request, '😔 insert "rsID" (ex-rs1921) 😔')
        return HttpResponseRedirect(reverse('search:main'))



def upload(request):
    global readfile
# not selected
    if request.FILES.__len__() == 0:
        messages.info(request, 'There are no files !')
        return HttpResponseRedirect(reverse('search:main'))
# in case not txt file selected
    uploadfile = request.FILES['file']
    if uploadfile.name.find('txt') < 0:
        messages.info(request, ' This is not txt file ! use txt file')
        return HttpResponseRedirect(reverse('search:main'))

    f = uploadfile.read().decode('utf8')
    data = StringIO(f)
    txtfile = pd.read_csv(data, header=None, dtype=str)
    txtfile.columns = ['rsID']

    if readfile.empty:
        read_file_from_csv()

# i want to keep the rsIDs what i insert
    result = pd.merge(txtfile, readfile, how='left', on=['rsID'])
# no i want to see only avaliable values(without null values)
    # result = pd.merge(txtfile, readfile, how='inner', on=['rsID'])


# no RSID matched with data
    if result.empty:
        messages.info(request, '😔 nothing to show 😔')
        return HttpResponseRedirect(reverse('search:main'))
# show result
    else:
        columnlist = ['rsID', 'CHR', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation']
        result = result[columnlist]
        result = result.fillna('N/A')
        dic = result.to_dict('records', into = OrderedDict)
        context = {'result': dic}
        return render(request, 'search/result.html', context)


def result_download(request):
    table = request.POST
    return HttpResponse(table)


def file_download(request):
    f = str(os.getcwd())+'/example.txt'
    response = HttpResponse(open(f, 'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]for_upload.txt"'
    return response
