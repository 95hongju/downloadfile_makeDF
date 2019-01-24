import search.fileDownOpen as fd
import mysql.connector
import schedule
import time


def connect_db():
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        passwd = "1234",
        database = "DS_table"
        )
        mycursor = mydb.cursor()
        return mycursor, mydb
    except Exception as e:
        print(e)
        return False


def update_database():
    fileOnURL = fd.find_date()
    print(fileOnURL)
    ###############
    mycursor, mydb = connect_db()
    sql_select = "SELECT * FROM search_downloadfilelist WHERE file_name='"+fileOnURL+"';"
    mycursor.execute(sql_select)
    result = mycursor.fetchall()

    if len(result) == 0:
    ###############
        filename = fileOnURL + '.vcf.gz'
        fd.down_process(filename)
        print(filename)
        sql = "INSERT INTO search_downloadfilelist(file_name, down_date) VALUES ('" + fileOnURL + "', NOW());"
        mycursor.execute(sql)
        mydb.commit()
        print('add file')
    else:
        print('dont need to download db')
    mydb.close()
    print('############################ done')


if __name__ == '__main__':
    schedule.every().sunday.at("04:00").do(update_database)
    #schedule.every().monday.at("11:48").do(update_database)
    while True:
        schedule.run_pending()
        time.sleep(1)
