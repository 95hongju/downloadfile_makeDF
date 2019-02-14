import schedule
import time
import requests
import pandas as pd
import sys
import snp.v2_html_from_snpedia as v2

def update_log():
    print(' - update SNPedia search log - ')

    try:
    #read log file
        file_read = pd.read_csv('./snp/log.txt', header=None, names=['rsID'])
    #match string(rs####)
        file_process = file_read[file_read.rsID.str.match('rs[0-9]+$')]
    #drop duplicated
        file_process = file_process.drop_duplicates()
        size = file_process['rsID'].size
        print(str(size) + ' files will update ...')
        print(file_process['rsID'])

    except:
        #end program
        print(' There are No LOG FILE ! ')
        sys.exit()


    if size == 0:
        #no data in logfile
        print('log file is clear ...')
        sys.exit()

    else:
        try:
            #read current database / append df
            db = pd.read_csv('./snp/final_db.csv', sep='\t')
            #drop duplicated (df - db)
            df = file_process[~file_process.rsID.isin(db.rsID)]
            if(df['rsID'].size == 0) :
                print('all rsIDs are already exist !!!')
                sys.exit()
            #apply function
            df['rawHTML'] = df['rsID'].apply(v2.gethtml)
            #append df
            db = db.append(df)

            #save database
            db.to_csv('./snp/final_db.csv', sep='\t', index=False)
            print(' - D O N E ! - ')
        except:
            print('error T-T')

    #print current time
    localtime = time.asctime(time.localtime(time.time()))
    print('Date : ' + localtime)

if __name__ =='__main__':
    schedule.every().sunday.at("04:00").do(update_log)
    #update_log()
    while True:
        schedule.run_pending()
        time.sleep(1)
