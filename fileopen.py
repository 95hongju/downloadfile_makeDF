import gzip
import urllib.request
import os
import io
import pandas as pd
import re
import datetime


# download vcf file & unzip

def download_file():
    print('download file ----')
# set url and open file
    url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz"
    filename = "clinvar.vcf.gz"
    outFileName = filename[:-3]
    response = urllib.request.urlopen(url)

    with open(outFileName, 'wb') as outfile:
        outfile.write(gzip.decompress(response.read()))

    print('download done')
    return outFileName


# extract data in vcf
# use the date and rename file
def vcf_rename(path):
    with open(path, 'r') as f:
        tmp = f.read()[:60]
        match = re.search('\d{4}-\d{2}-\d{2}', tmp)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        newname = 'clinvar_'+''.join(str(date).split('-'))+'.vcf'
        os.rename(path, newname)
        print('newname ->', newname)
        return newname


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


outFileName = download_file()
saved_file = vcf_rename(outFileName)
# saved_file = 'clinvar_20181217.vcf'
print('reading vcf ...')
df = read_vcf(saved_file)
print('applying function...')
# create new columns
df[['RS', 'CLNSIG']] = df['INFO'].apply(extract_rs_clnsig)
print('drop column...')

# drop ['info'] column
df = df.drop('INFO', axis=1)

# save it as csv file
df.to_csv(saved_file+'.csv', index=False, sep='\t')

print("done ! check the file")
