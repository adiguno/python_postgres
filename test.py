import psycopg2
import uuid

# Connect to your postgres DB
# TODO add these config to a configuration file, to enable prod/dev environments
# TODO wrap cursor connect and other operations with try/catch
def connect():
    ''' return the connection '''
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="test-go-db",
        user="postgres",
        password="postgres")

def get_cursor(conn):
    # Open a cursor to perform database operations
    return conn.cursor()

def get_db_version(cursor):
    # display the PostgreSQL database server version
    print('PostgreSQL database version:')
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

def get_all_user(cursor):
    # Execute a query
    cursor.execute("SELECT * FROM USER")
    # Retrieve query results
    records = cursor.fetchall()
    return records

def insert_user(cursor, user, conn):
    sql = "INSERT INTO all_user (\"UUID\", \"USERNAME\", \"POINTS\") VALUES (%s, %s, %s)"
    # query = sql.format(user.uuid, user.username, user.points)
    # print(query)
    # cur.execute('INSERT INTO src_event (location_id, catname, title, name) VALUES (%s, %s, %s, %s)', (1441, 'concert', item['title'], item['artists']))
    x = cursor.execute(sql, (str(user.uuid), user.username, user.points))

    conn.commit()

    return x

def close_cursor(cursor):
    # close the communication with the PostgreSQL
    cursor.close()

class User:
    uuid = ""
    username = ""
    points = 0

    def __init__(self, username="", points=0):
        self.uuid = uuid.uuid4()
        self.username = username
        self.points = points

    def __str__(self):
        return "User {" + str(self.uuid) + "} has username {" + self.username + "} with {" + str(self.points) + "} points"

if __name__ == "__main__":
    user = User("asdf")
    print(user)

    try: 
        conn = connect()
        cur = get_cursor(conn)

        insert_response = insert_user(cur, user, conn)
        print(insert_response)

        records = get_all_user(cur)
        for record in records:
            print(record)
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)