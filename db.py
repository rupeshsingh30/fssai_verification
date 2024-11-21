
import psycopg2

from config import *  


def dbConnection():
    conn = psycopg2.connect(
        dbname='postgres', 
        user='postgres',
        password='admin',
        host='localhost',
        port="5432"
        )
    cursor=conn.cursor()

    return conn,cursor

# list = ['1', 'Sleepy Owl Coffee Pvt. Ltd.', 'Hadbasat No. 161 - Khewat No./ Khata No. 495/510, 792/841, Sector 76, Groz Tolls Link Road, Village Kherki Dhola, Tehsil Manesar,Gurugram,Haryana-122004', '13321999000263', 'Central License', 'Active', 'View Products']
def insertQuery(conn,cursor,list):
    cursor.execute(f""" insert into public."fssai_table"(company_name,premises_address,license_number,license_type,valid,timestamp)  values('{list[1]}','{list[2]}','{list[3]}','{list[4]}','{list[5]}','{list[-1]}' )""")
    conn.commit()
    print('inserted data')


# conn, cursor = dbConnection()
# insertQuery(conn,cursor,list)