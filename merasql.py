import mysql.connector as mc


def connection(h="localhost", u="root", p="Aditya2612"):
    # database ke saath connection
    try:
        co = mc.connect(host=h, user=u, passwd=p)
        cu = co.cursor()
        return cu, co

    except mc.InterfaceError as e:
        print(e)
        print("Your connection to database was interrupted.\
Check for the proper version of SQL and python, and restart the application.")


try:
    curs, conn = connection()
except mc.ProgrammingError as e:
    print(e)
    print("Make sure you have entered the correct password.")
    connection(p=input("Enter the password again:"))


def db_creation(dbname, cur=curs, con=conn):
    # database banane ke liye
    cur.execute(f"create database if not exists {dbname}")
    con.commit()


def usedb(dbname, cur=curs, con=conn):
    # database use krne ke liye
    cur.execute(f"use {dbname}")


def table_creation(struc, cur=curs, con=conn):
    # table banane ke liye
    cur.execute(f"create table if not exists {struc}")
    con.commit()


def insert(table, fieldlist, data, cur=curs, con=conn):
    # table me data daalne ke liye
    cur.execute(f"insert into {table}{fieldlist} values {data}")
    con.commit()


def read(table, fields='*', where=None, groupby=None, having=None, orderby=None, cur=curs):
    # table se data uthane ke liye
    query = f"select {fields} from {table}"
    if where is not None:
        query = query + f" where {where}"
    if groupby is not None:
        query = query + f" group by {groupby}"
    if having is not None:
        query = query + f" having {having}"
    if orderby is not None:
        query = query + f" order by {orderby}"

    cur.execute(query)
    return cur.fetchall()


def update(table, field, value, where=None, cur=curs, con=conn):
    # table me data update karne ke liye
    query = f"update {table} set {field}={value}"
    if where is not None:
        query = query + f" where {where}"

    cur.execute(query)
    con.commit()


def delete(table, where=None, cur=curs, con=conn):
    # table me data delete karne ke liye
    query = f"delete from {table}"
    if where is not None:
        query = query + f"where {where}"

    cur.execute(query)
    con.commit()


def drop(typ, name, cur=curs, con=conn):  # kisi chez ko drop krne ke liye
    if typ == "d":
        cur.execute(f"drop database {name}")
    if typ == "t":
        cur.execute(f"drop table {name}")
    else:
        print("You did not enter a valid type.")
        drop(typ=input("Enter type as \'t\' or \'d\':"), name=name)

    con.commit()
    
