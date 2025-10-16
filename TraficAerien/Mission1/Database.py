import pymysql
import sqlalchemy

def connect_mydb(): 
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='db_airport',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection
def connect_db():
    connection = sqlalchemy.create_engine("mysql+pymysql://root:@localhost/db_airport?charset=utf8mb4")
    host='localhost',
    user='root',
    password='',
    database='db_airport'
    #connection = sqlalchemy.create_engine("mysql+pymysql://user:pass@some_mariadb/db_airport?charset=utf8mb4")
    return connection

def write_db(connection,rqt):
    with connection.cursor() as cursor:
        # Create a new record
        #sql = "INSERT INTO `user` (`name`, `solde`,`level`) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE `solde`=%s,`level`=%s"
        cursor.execute(rqt)

    connection.commit()
    

def read_one(connection, rqt,arg):
    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute(rqt, (arg, ))
        result = cursor.fetchone()
        #if(result == None):
        #    result = write_db(connection, name, 10,1)
        return result



def read_all(connection, sql,arg):
    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute(sql, (arg, ))
        result = cursor.fetchall()
        #if(result == None):
        #    result = write_db(connection,)
        return result
   
