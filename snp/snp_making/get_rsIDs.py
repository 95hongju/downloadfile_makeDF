# get rsID from each category
# https://www.snpedia.com/index.php/Special:Categories

import pandas as pd
import requests
import re

p = re.compile('Rs[0-9]+')

def make_txtfile(category):
    #api parameters
    S = requests.Session()
    URL = "https://www.snpedia.com/api.php"


    # loop start 
    for c in category:
        #temp dataframe
        print(c+' start !')
        temp = pd.DataFrame(columns=['ns','pageid','title'])

        #params for 'cmcontinue'
        nxt = ""
        done=True

        while(done):
            PARAMS = {
            'action': "query",
            'list': "categorymembers",
            'cmtitle': "Category:"+c,
            'cmlimit':200,
            'cmcontinue':nxt,
            'format': "json"
            }

            #get api
            R = S.get(url=URL, params=PARAMS)
            data = R.json()

            try:
                nxt=data['continue']['cmcontinue']
                #print(nxt)
            except:
                done=False
                #print('last time ----')

            table = pd.DataFrame.from_dict(data['query']['categorymembers'])
            rs=table.loc[table['title'].str.contains('Rs')]

            temp = temp.append(rs)
        
        print('total size : '+ str(temp.title.size))
        temp['title'].to_csv('./rs_pack/'+c+'.txt',sep='\t',index=False,header=['rs'])


def remove_other(row):
    global p

    v =p.match(row)
    return v.group() if v else 'Null'


def concat_tables(category):
    """
    combine tables from categories(make_txtfile function's output)
    make one table
    Rs -> rs
    drop duplicates
    """

    #base
    t = pd.DataFrame(columns=['rs'])

    #loop for merge
    for c in category:
        table_c = pd.read_csv('./rs_pack/'+c+'.txt')
        print(str(t.size)+' + '+str(table_c.size)+' = '+str(t.size+table_c.size))
        t = pd.merge(t, table_c, how='outer',on='rs')
        print(t.size)

    #match
    t['rsID'] = t['rs'].apply(remove_other)

    #drop column & duplicates
    t = t.drop(columns=['rs'])
    t['rsID'] = t['rsID'].str.lower()
    t = t.drop_duplicates()

    print('made table += categories')
    t.to_csv('categories_1.txt',sep='\t',index=False)
    print(t.size)
    




def main():
    
    category = ['GWAS', 'Has_Report_GE','Has_genotype','Has_population','In_dbSNP','Is_a_genotype','SNPs_on_chromosome_4']

    #make_txtfile(category)
    concat_tables(category)

if __name__ == "__main__":
    main()
