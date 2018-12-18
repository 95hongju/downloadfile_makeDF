import gzip
import urllib.request
import os
import io
import pandas as pd
import re
import datetime


# before download the file, check the date(latest file upload date)

#problem ... what if filename is 20181217 but updated date is 20181205,,?
def find_date():
    print('check the time ...')
    url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/"
    response = urllib.request.urlopen(url)
    filelist=response.read()
    match = re.search('\d{4}\d{2}\d{2}', str(filelist))
    date = datetime.datetime.strptime(match.group(), '%Y%m%d').date()
    file_date=''.join(str(date).split('-'))

    filename='clinvar_'+file_date+'.vcf.gz'
    print(filename)
    return download_file(filename)


# download vcf file & unzip
def download_file(filename):
    print('download file ...')
# set url and open file
    url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/"+filename
    response = urllib.request.urlopen(url)
    outFileName = filename[:-3]

    with open(outFileName, 'wb') as outfile:
        outfile.write(gzip.decompress(response.read()))

    print('download done ...')
    return outFileName


# this function is for vcf to dataframe
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_table(io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
        'QUAL': str, 'FILTER': str, 'INFO': str}).rename(columns={'#CHROM': 'CHROM'})


# extract rsID and CLNSIG from the ['INFO']
def extract_rs_clnsig(row):
    list = row.split(';')
    rs = sig = ''
    for i in list:
        if 'CLNSIG' in i:
            sig = i.split('=')[1]
        if 'RS' in i:
            rs = i.split('=')[1]
    return pd.Series([rs, sig])


saved_file=find_date()
# saved_file = 'clinvar_20181217.vcf'
print('reading vcf ...')
df = read_vcf(saved_file)
print('applying function ...')
# create new columns
df[['RS', 'CLNSIG']] = df['INFO'].apply(extract_rs_clnsig)
print('drop column ...')

# drop ['info'] column
df = df.drop('INFO', axis=1)

# save it as csv file
df.to_csv(saved_file[:-4]+'.csv', index=False, sep='\t')

print("done ! check the file")
