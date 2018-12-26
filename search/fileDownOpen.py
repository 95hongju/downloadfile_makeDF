import gzip
import urllib.request
import io
import pandas as pd
import re
import os
import shutil



# before download the file, check the date(latest file upload date)
def find_date():
    print('check the date ...')
    url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/"
    response = urllib.request.urlopen(url)
    filelist = response.read()
    match = re.search(r'clinvar_\d{4}\d{2}\d{2}', str(filelist))

    #filename = match.group()+'.vcf.gz'
    return  match.group()


# download vcf file & unzip
def download_file(filename):
    print('download file ...')
# set url and open file
    url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/"+filename
    response = urllib.request.urlopen(url)
    outFileName = filename[:-3]
    print(outFileName)
    try:
        with open(outFileName, 'wb') as outfile:
            outfile.write(gzip.decompress(response.read()))
            currpath=os.getcwd()+'/search/data/'
            shutil.move(outFileName, currpath)
        print('download done ...')
        return './search/data/'+outFileName
    except Exception as err:
        print(err)
        return './search/data/'+outFileName



# this function is for vcf to dataframe
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_table(io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': str, 'ID': str, 'REF': str, 'ALT': str,
        'QUAL': str, 'FILTER': str, 'INFO': str}).rename(columns={'#CHROM': 'CHR'})


# extract rsID and CLNSIG from the ['INFO']
def extract_rs_clnsig(row):
    list = row.split(';')
    rs = sig = ''
    for i in list:
        if 'CLNSIG' in i:
            sig = i.split('=')[1]
        if 'RS' in i:
            rs = 'rs' + i.split('=')[1]
    return pd.Series([rs, sig])


def down_process(filename):
    saved_file = download_file(filename)
    print('savedfile ',saved_file)
    print('reading vcf ...')
    df = read_vcf(saved_file)
    print('applying function ...')
    # create new columns
    df[['rsID', 'clinvar Annotation']] = df['INFO'].apply(extract_rs_clnsig)
    print('drop column ...')

    # drop ['info'] column
    df = df.drop(['INFO','ID'], axis=1)

    # save it as csv file
    df.to_csv(saved_file[:-4]+'.csv', index=False, sep='\t')

    print("done ! check the file")

def main():
    pass

if __name__ == '__main__':
    main()
