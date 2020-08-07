import mysql.connector
from mysql.connector import Error


class YelpContext:

    connection = None

    def __init__(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='yelp',
                                                 user='root',
                                                 password='kutyboy98')
            if connection.is_connected():
                self.connection = connection
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

    def disconnect(self):
        if (self.connection.is_connected()):
            self.disconnect()
            print('MySQL connection is closed')


class Reponsitory:

    dbcontext = None
    table_name = ''
    properties = []

    def __init__(self, _dbcontext, _table_name, _properties):
        self.dbcontext = _dbcontext
        self.table_name = _table_name
        self.properties = _properties

    def disconnect(self):
        self.dbcontext.disconnect()

    def get(self):
        query = f'Select * from {self.table_name}'
        cursor = self.dbcontext.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def post(self, _value):
        try:
            properties = ','.join(self.properties)
            values = ','.join(['%s' for item in self.properties])
            query = f'''
                        Insert into {self.table_name} ({properties})
                        values ({values})
                    '''
            cursor = self.dbcontext.connection.cursor()
            cursor.execute(query, _value)
            self.dbcontext.connection.commit()
            return True
        except mysql.connector.Error as error :
            print(f'Failed to insert record to database. {error}')
            self.dbcontext.connection.rollback()
            return False


class CategoryDbSet(Reponsitory):

    def __init__(self, _dbcontext):
        tbname = 'category'
        properties = ['id','name','label']
        super(CategoryDbSet, self).__init__(_dbcontext, tbname, properties)


class RestaurantDbSet(Reponsitory):

    def __init__(self, _dbcontext):
        tbname = 'restaurant'
        properties = [
                        'id', 'name', 'code',
                        'region', 'category_id', 'url',
                        'star', 'review', 'address',
                        'imgs', 'services'
                     ]
        super(RestaurantDbSet, self).__init__(_dbcontext, tbname, properties)

    def check_exist(self, _code):
        query = f'Select * from {self.table_name} where code = "{_code}"'
        cursor = self.dbcontext.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            return True
        return False

class ReviewDbSet(Reponsitory):

    def __init__(self, _dbcontext):
        tbname = 'review'
        properties = [
                        'id', 'restaurant_id', 'content',
                        'imgs', 'review', 'usefull',
                        'funny', 'cool', 'review_time'
                     ]
        super(ReviewDbSet, self).__init__(_dbcontext, tbname, properties)

    def check_exist(self, _id):
        query = f'Select * from {self.table_name} where id = "{_id}"'
        cursor = self.dbcontext.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            return True
        return False

