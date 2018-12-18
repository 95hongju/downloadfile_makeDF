from django.shortcuts import render
from django.http import HttpResponse

from .models import downloadFileList


# Create your views here.
def main(request):
    # if the latest file in database is using
    latest_file = downloadFileList.objects.latest('down_date')
    if latest_file.using == 1:
        print("now using")

    # current file != latest_file
    else:
        #do something
        print('not using')

    context={'latest_file':latest_file}
    return render(request, 'search/index.html',context)
