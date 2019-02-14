from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from io import StringIO
from collections import OrderedDict
import os
import pandas as pd
import snp.v2_html_from_snpedia as v2

db = pd.read_csv('./snp/final_db.csv', sep='\t')

def main(request):
    return render(request, 'snp/main.html')

def reportmaker(rsID):
    global db
    db.fillna('')
    print(rsID,'-----------------')
    t = db.loc[db['rsID'] == rsID]
    if(t['rsID'].size == 0):
        #using API
        print('\t\tusing API')
        f = open('./snp/log.txt','a+')
        f.write(rsID+'\n')
        f.close()
        report = v2.making_table_process(rsID)
    else :
        #using DB
        print('\t\tusing DB')
        rawHTML =[]
        rawHTML.append(t['rawHTML'].values[0])
        rs, ge, tb, ds = v2.make_report(t['rsID'].values[0], rawHTML)
        report = v2.make_OrderedDict(rs, ge, tb, ds)
        print('rsID - '+ rsID + ' - DONE !')
    return report

def file_report(request):
# not selected
    if request.FILES.__len__() == 0:
        messages.info(request, 'There are no files !')
        return HttpResponseRedirect(reverse('snp:main'))
# in case not txt file selected
    uploadfile = request.FILES['file']
    if uploadfile.name.find('txt') < 0:
        messages.info(request, ' This is not txt file ! use txt file')
        return HttpResponseRedirect(reverse('snp:main'))
#if file uploads successfully
    f = uploadfile.read().decode('utf8')
    f = f.replace('\r','\n')
    f_list=f.split('\n')
    readfile = [r.replace('\n','') for r in f_list]
    readfile = list(filter(None,readfile))
    print('DATA ---> ',readfile)

    reports = []
    for rs in readfile:
        reports.append(reportmaker(rs))
    context = {'reports': reports,'txt':' - '}

    return render(request, 'snp/report_snp.html', context)


def one_report(request):
    rsID = request.POST['inputRS']
    if 'rs' in rsID:
        reports=[]
        reports.append(reportmaker(rsID))
        #print(reports)
        context = {'reports': reports,'txt':' - '}
        return render(request, 'snp/report_snp.html', context)
    else :
        messages.info(request, '😔 insert "rsID" (ex-rs6152) 😔')
        return HttpResponseRedirect(reverse('snp:main'))


def file_download(request):
    f = str(os.getcwd())+'/examples/example_snp.txt'
    response = HttpResponse(open(f, 'rb'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="[sample]file_upload(snp).txt"'
    return response


def usage(request):
    return render(request, 'snp/usage.html')
