from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import downloadFileList
from io import StringIO
import pandas as pd
import os

import search.fileDownOpen as fd

columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'RS', 'CLNSIG']
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
    else:
        usingfile = downloadFileList.objects.latest('down_date')
        qr = downloadFileList.objects.filter(file_name=fileOnURL)
        if len(qr) == 0:
            messages.info(request, '❗❗ need update ❗❗ ( it will take 2-3 mins)')
        if readfile.empty:
            read_file_from_csv()


    context = {'currUsingFile': usingfile}
    return render(request, 'search/index.html', context)


def read_file_from_csv():
    global readfile

    usingfile = downloadFileList.objects.latest('down_date')
    print('read dataframe....')
    path = os.path.join(os.path.dirname(__file__))+'/data/'+usingfile.file_name+'.csv'
    dtypes = {'CHROM': str, 'POS': str, 'ID': str, 'REF': str, 'ALT': str, 'QUAL': str, 'FILTER': str, 'RS': str, 'CLNSIG': str}
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
    result = readfile.loc[readfile['RS'] == keyword]
    if result.empty:
        messages.info(request, '😔 nothing to show 😔')
        return HttpResponseRedirect(reverse('search:main'))
    else:
        result.columns = ['RS','CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'CLNSIG']
        dic = result.to_dict('index')
        context = {'result': dic}
        return render(request, 'search/result.html', context)


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
    txtfile.columns = ['RS']

    if readfile.empty:
        read_file_from_csv()

# i want to keep the rsIDs what i insert
    result = pd.merge(txtfile, readfile, how='left', on=['RS'])
    result.columns = ['RS','CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'CLNSIG']
# no i want to see only avaliable values(without null values)
    # result = pd.merge(txtfile, readfile, how='left', on=['RS'])


# no RSID matched with data
    if result.empty:
        messages.info(request, '😔 nothing to show 😔')
        return HttpResponseRedirect(reverse('search:main'))
# show result
    else:
        dic = result.to_dict('index')
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
