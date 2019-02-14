import pandas as pandas
gs12=pd.read_csv('GSA_(v1.2).txt',sep='\t')
gs12['GSA v1.2']='O'
gs21=pd.read_csv('GSAMD_(v2.1).txt',sep='\t')
gs21['GSAMD v2.1']='O'

gs12 = gs12.rename(columns={'ID':'rsID', 'CHROM':'CHR'})
gs21 = gs21.rename(columns={'ID':'rsID', 'CHROM':'CHR'})

gs_table = pd.merge(gs12,gs21, how='outer')

gs_table.to_csv('gs12_gs21.csv', sep='\t', index=False)