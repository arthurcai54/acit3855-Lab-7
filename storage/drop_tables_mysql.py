import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="Mahomeboy#15", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
                DROP TABLE sale_item, num_sales
            ''')
            
db_conn.commit()
db_conn.close()