import mysql.connector
import openpyxl

def dataquery(schema, query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
    )

    cursor = mydb.cursor()
    cursor.execute("use {};".format(schema))
    if ("update" in query.lower()) or ("insert" in query.lower()):
        cursor.execute("{};".format(query))
        mydb.commit()
    else:
        date = []
        cursor.execute("{};".format(query))
        data = cursor.fetchall()
        for d in data:
            print(d)
        mydb.close()
        return data



print(dataquery("pavan","select test_id, user_name, user_password, message, login from login_test"))
