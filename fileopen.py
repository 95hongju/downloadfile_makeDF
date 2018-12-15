import gzip
import urllib.request
import os
import io
import pandas as pd
import re
import datetime


print('download file ----')
# set url and open file
url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz"
filename = "clinvar.vcf.gz"
outFilePath = filename[:-3]
response = urllib.request.urlopen(url)

with open(outFilePath, 'wb') as outfile:
    outfile.write(gzip.decompress(response.read()))
    print(type(outfile))


print('done')

# extract data in vcf
# use the date and rename file
def vcf_rename(path):
    with open(path, 'r') as f:
        tmp = f.read()[:100]
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
        dtype = {'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
        'QUAL': str, 'FILTER': str, 'INFO': str}).rename(columns={'#CHROM': 'CHROM'})


# extract rsID and CLNSIG from the ['INFO']
def extract(row):
    list = row.split(';')
    rs = sig = ''
    for i in list:
        if 'CLNSIG' in i:
            sig = i.split('=')[1]
        if 'RS' in i:
            rs = i.split('=')[1]
    return pd.Series([rs, sig])


saved_file = vcf_rename(outFilePath)
df = read_vcf(saved_file)

# create new columns
df[['RS', 'CLNSIG']] = df['INFO'].apply(extract)

# drop ['info'] column
df = df.drop('INFO', axis=1)

print(df.head())
df.to_csv('friday.csv')
