import mysql.connector as mc
import sqlite3 as sq
import pandas as pd


class SQL:
    def __init__(self, connectivity="sqlite", h="localhost", u="root", p="Aditya2612", d=None):
        # database ke saath connection
        try:
            if connectivity == "mysql":
                self.con = mc.connect(host=h, user=u, passwd=p, database=d)
                self.cur = self.con.cursor()
            if connectivity == "sqlite":
                self.con = sq.connect(f"{d}.db")
                self.cur = self.con.cursor()
        except mc.InterfaceError as e:
            print(e)
            print("Your connection to database was interrupted.\
        Check for the proper version of SQL and python, and restart the application.")

    def cust_select(self, tables, fields='*', where=None, groupby=None, having=None, orderby=None):
        # table se data uthane ke liye
        query = f"select {fields} from {tables}"
        if where is not None:
            query = query + f" where {where}"
        if groupby is not None:
            query = query + f" group by {groupby}"
        if having is not None:
            query = query + f" having {having}"
        if orderby is not None:
            query = query + f" order by {orderby}"

        self.cur.execute(query)
        return self.cur.fetchall()

    def drop(self, typ, name):  # kisi cheez ko drop krne ke liye
        if typ == "db":
            self.cur.execute(f"drop database {name}")
        if typ == "table":
            self.cur.execute(f"drop table {name}")
        else:
            print("You did not enter a valid type.")
            SQL.drop(self, typ=input("Enter type as \'t\' or \'d\':"), name=name)

        self.con.commit()


class DataBase(SQL):
    def __init__(self, connection, name):
        super().__init__()
        self.name = name
        self.cur = connection.cur
        self.con = connection.con
        self.cur.execute(f"create database if not exists {name}")
        self.con.commit()

    def usedb(self):
        # database use krne ke liye
        self.cur.execute(f"use {self.name}")


class Table(SQL):
    def __init__(self, structure, database, name):
        super().__init__()
        database.usedb()
        self.struc = structure
        self.dbase = database
        self.name = name
        self.cur = database.cur
        self.con = database.con
        self.cur.execute(f"create table if not exists {self.name}({structure})")
        self.con.commit()
        self.flist = []
        for x in self.desc():
            self.flist.append(x[0])

    def desc(self):
        self.cur.execute(f"desc {self.name}")
        return self.cur.fetchall()

    def insert(self, data):
        # table me data daalne ke liye
        self.cur.execute(f"insert into {self.name} values {data}")
        self.con.commit()

    def select(self, fields='*', where=None, groupby=None, having=None, orderby=None):
        # table se data uthane ke liye
        query = f"select {fields} from {self.name}"
        if where is not None:
            query = query + f" where {where}"
        if groupby is not None:
            query = query + f" group by {groupby}"
        if having is not None:
            query = query + f" having {having}"
        if orderby is not None:
            query = query + f" order by {orderby}"

        self.cur.execute(query)
        return self.cur.fetchall()

    def update(self, field, value, where=None):
        # table me data update karne ke liye
        query = f"update {self.name} set {field}={value}"
        if where is not None:
            query = query + f" where {where}"

        self.cur.execute(query)
        self.con.commit()

    def delete(self, where=None):
        # table me data delete karne ke liye
        query = f"delete from {self.name}"
        if where is not None:
            query = query + f" where {where}"

        self.cur.execute(query)
        self.con.commit()

    def view_data(self):
        df = pd.DataFrame(self.select())
        if df.empty:
            return "-> Empty table."
        else:
            df.columns = self.flist
            return df

    def insert_data(self):
        info = self.desc()
        data = []
        try:
            for x in info:
                dtype = x[1]
                if "int" in dtype:
                    val = int(input(f"Enter {x[0]}(numeric): "))
                if "float" in dtype:
                    val = float(input(f"Enter {x[0]}(decimal): "))
                if dtype == "date":
                    val = f'{input(f"Enter {x[0]}(yyyy-mm-dd): ")}'
                if "varchar" in dtype:
                    val = f'{input(f"Enter {x[0]}: ")}'
                data.append(val)
        except ValueError or mc.DataError:
            print("\n-> Please enter a valid value!")
            self.insert_data()
        except mc.IntegrityError:
            print(f"\n-> Please do not enter duplicate value for {info[0][0]}!")
            self.insert_data()
        self.insert(data=tuple(data))

    def update_data(self):
        info = self.desc()
        print("\nFields of the table are -: ")
        for x in info:
            print(x[0])
        clm = input("Enter field name for which you want to change data: ")
        dtype = ""
        for x in info:
            if x[0] == clm:
                dtype = x[1]
                break
        try:
            if dtype == "":
                print("\n-> Please enter column from given list!")
                self.update_data()
            if dtype == "int":
                val = int(input(f"\nEnter new {clm}(numeric): "))
            if dtype == "float(9,2)":
                val = float(input(f"\nEnter new {clm}(numeric): "))
            if dtype == "date":
                val = f'{input(f"\nEnter new {clm}(as yyyy-mm-dd): ")}'
            if dtype == "str":
                val = f'{input(f"\nEnter new {clm}: ")}'
        except ValueError:
            print("\n-> Please enter a valid value!")
            self.update_data()
        c = input('''\nDo you want to change it for all rows?
    1. Yes
    2. No
    Enter choice: ''')
        if c == "1":
            cod = None
        elif c == "2":
            print("\n-> Please give the condition to be applied (Example condition-> Item_id = 5).")
            cod = input(f"Enter condition: ")
        else:
            print("\n-> Please enter a valid value!")
            self.update_data()
        self.update(field=clm, value=val, where=cod)

    def delete_data(self):
        info = self.desc()
        cid = int(input(f"\nEnter {info[0][0]} of the row you want to delete: "))
        c = input('''\n-> Are you sure you want to delete the data?
    1. Yes
    2. No
    Enter choice: ''')
        if c == "1":
            self.delete(where=f"{info[0][0]} = {cid}")
            print("-> Data deleted successfully.")
        elif c == "2":
            print("\n-> Your data is safe.")
        else:
            print("\n-> Please enter a valid value!")
            self.delete_data()
