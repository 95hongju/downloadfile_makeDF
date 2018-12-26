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
    filename = fileOnURL + '.vcf.gz'
    fd.down_process(filename)
    print(filename)
    mycursor, mydb = connect_db()
    sql = "insert into search_downloadfilelist(file_name, down_date) values ('" + fileOnURL + "', NOW());"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    print('add file')
    mydb.close()


if __name__ == '__main__':
    schedule.every().sunday.at("04:00").do(update_database)
    #schedule.every().wednesday.at("14:01").do(update_database)
    while True:
        schedule.run_pending()
        time.sleep(1)
