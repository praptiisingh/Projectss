import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")
for table in cursor:
    print(table)

conn.close()