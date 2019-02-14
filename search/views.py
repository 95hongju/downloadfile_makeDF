
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

columns = ['CHR', 'POS',  'REF', 'ALT', 'QUAL', 'FILTER', 'rsID', 'clinvar Annotation','GSA v1.2','GSAMD v2.1']
readfile = pd.DataFrame(columns=columns)
print(readfile.empty)

# Create your views here.
def main(request):
    global readfile

    # get queryset
    q = downloadFileList.objects.all()

    # if empty queryset, download file from url
    # this will be take 2-3 mins
    if len(q) == 0:
    # check the name from the urls
        fileOnURL=fd.find_date()
        print('-----> ',fileOnURL)
        filename = fileOnURL+'.vcf.gz'
        fd.down_process(filename)
        newone=downloadFileList(file_name=fileOnURL)
        newone.save()

    if readfile.empty:
        read_file_from_csv()

    usingfile = downloadFileList.objects.latest('down_date')


    context = {'currUsingFile': usingfile}
    return render(request, 'search/index.html', context)


def read_file_from_csv():
    global readfile

    usingfile = downloadFileList.objects.latest('down_date')
    print('read dataframe....')
    path = os.path.join(os.path.dirname(__file__))+'/data/'+usingfile.file_name+'.csv'
    print(path)
    dtypes = {'CHR': str, 'POS': str, 'REF': str, 'ALT': str, 'QUAL': str, 'FILTER': str, 'rsID': str, 'clinvar Annotation': str, 'GSA v1.2':str,'GSAMD v2.1':str}
    readfile = pd.read_csv(path, delimiter='\t', dtype=dtypes)



def searchRS(request):
    global readfile
    if readfile.empty:
        read_file_from_csv()

    keyword = request.POST['srchkeyword']
    if 'rs' in keyword:
        result = readfile.loc[readfile['rsID'] == keyword]
        if result.empty:
            messages.info(request, 'rs : 😔 nothing to show 😔')
            return HttpResponseRedirect(reverse('search:main'))
        else:
            columnList = ['rsID','CHR', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation','GSA v1.2','GSAMD v2.1']
            result = result[columnList]
            result = result.fillna('N/A')
            dic = result.to_dict('records', into=OrderedDict)
            context = {'result': dic}
            return render(request, 'search/result.html', context)

    else:
        messages.info(request, '😔 insert "rsID" (ex-rs1921) 😔')
        return HttpResponseRedirect(reverse('search:main'))



def uploadRS(request):
    global readfile
# not selected
    if request.FILES.__len__() == 0:
        messages.info(request, 'There are no files !')
        return HttpResponseRedirect(reverse('search:main'))
# in case not txt file selected
    uploadfile = request.FILES['file']
    if uploadfile.name.find('csv') < 0:
        messages.info(request, ' This is not csv file ! csv txt file')
        return HttpResponseRedirect(reverse('search:main'))

    f = uploadfile.read().decode('utf8')
    data = StringIO(f)
    df = pd.read_csv(data, dtype=str)
    df.columns = ['rsID']
    print(df)

    if readfile.empty:
        read_file_from_csv()

# i want to keep the rsIDs what i insert
    result = pd.merge(df, readfile, how='left', on=['rsID'])


# no RSID matched with data
    if result.empty:
        messages.info(request, 'rs : 😔 nothing to show 😔')
        return HttpResponseRedirect(reverse('search:main'))
# show result
    else:
        columnList = ['rsID','CHR', 'POS',  'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation','GSA v1.2','GSAMD v2.1']
        result = result[columnList]
        result = result.fillna('N/A')
        dic = result.to_dict('records', into=OrderedDict)
        context = {'result': dic}
        return render(request, 'search/result.html', context)



def file_downloadRS(request):
    f = str(os.getcwd())+'/examples/example_search_rsid.csv'
    response = HttpResponse(open(f, 'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(rsID).csv"'
    return response
##############################################################################

def searchPC(request):
    global readfile
    if readfile.empty:
        read_file_from_csv()

    srchPOS = request.POST['srchPOS']
    srchCHR = request.POST['srchCHR']
    if srchCHR =='':
        result = readfile.loc[readfile['POS'] == srchPOS]
    elif srchPOS =='':
        messages.info(request, 'p/c : 😔 input POS 😔')
        return HttpResponseRedirect(reverse('search:main'))
    else:
        result = readfile.loc[(readfile['POS'] == srchPOS) & (readfile['CHR'] == srchCHR)]

    if result.empty:
        messages.info(request, 'p/c : 😔 nothing to show 😔')
        return HttpResponseRedirect(reverse('search:main'))
    else:
        columnList = ['rsID','CHR', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation','GSA v1.2','GSAMD v2.1']
        result = result[columnList]
        result = result.fillna('N/A')
        dic = result.to_dict('records', into=OrderedDict)
        context = {'result': dic}
        return render(request, 'search/result.html', context)




def uploadPC(request):
    global readfile
# not selected
    if request.FILES.__len__() == 0:
        messages.info(request, 'There are no files !')
        return HttpResponseRedirect(reverse('search:main'))
# in case not txt file selected
    uploadfile = request.FILES['file']
    if uploadfile.name.find('csv') < 0:
        messages.info(request, ' This is not csv file ! use csv file')
        return HttpResponseRedirect(reverse('search:main'))

    f = uploadfile.read().decode('utf8')
    data = StringIO(f)
    df = pd.read_csv(data, dtype={'CHR':str,'POS':str}, sep='\t')

    if readfile.empty:
        read_file_from_csv()

# i want to keep the rsIDs what i insert
    try:
        result = pd.merge(df, readfile, how='left', on=['CHR','POS'])
    # no RSID matched with data
        if result.empty:
            messages.info(request, 'p/c : 😔 nothing to show 😔')
            return HttpResponseRedirect(reverse('search:main'))
    # show result
        else:
            columnList = ['rsID','CHR', 'POS',  'REF', 'ALT', 'QUAL', 'FILTER', 'clinvar Annotation','GSA v1.2','GSAMD v2.1']
            result = result[columnList]
            result = result.fillna('N/A')
            dic = result.to_dict('records', into=OrderedDict)
            context = {'result': dic}
            return render(request, 'search/result.html', context)
    except Exception as e:
        print(e)
        messages.info(request, 'check the file ! [ '+ str(e) + ']')
        return HttpResponseRedirect(reverse('search:main'))


def file_downloadPC(request):
    f = str(os.getcwd())+'/examples/example_search_pc.csv'
    response = HttpResponse(open(f, 'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(POS_CHR).csv"'
    return response


def usage(request):
    return render(request, 'search/usage.html') 
