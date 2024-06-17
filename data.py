# majdooron ko bulawa
import pandas as pd
import pymysql
import sqlalchemy as sa
import matplotlib.pyplot as plt


class Database:
    def __init__(self, pwd, dbname):
        self.pwd = pwd
        self.dbname = dbname
        self.engine = sa.create_engine(f"mysql+pymysql://root:{pwd}@localhost:3306/{dbname}")

    def read(self, table, fields='*', where=None, groupby=None, having=None, orderby=None):
        """
        This function can be used to fetch data from a sql table in the form of a dataframe.
        :param table: str- table's name
        :param fields: str- name of Fields required separated by ', '
        :param where: str(optional)- where condition in sql query
        :param groupby: str(optional)- name of field(s) to be grouped by
        :param having: str(optional)- having condition of sql query
        :param orderby: str(optional)- name of field to be ordered by
        :return: dataframe- output of the sql query
        """
        query = f"select {fields} from {table}"
        if where is not None:
            query = query + f" where {where}"
        if groupby is not None:
            query = query + f" group by {groupby}"
        if having is not None:
            query = query + f" having {having}"
        if orderby is not None:
            query = query + f" order by {orderby}"

        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            print(f"Error {e} occurred.")

    def insert(self, table, values):
        """
        This function can be used to insert data into a sql table.
        :param table:str- Name of the table in which data is to be entered
        :param values: list- List of values to be entered in the table
        :return: None
        """
        try:
            df = pd.DataFrame(values)
            df.to_sql(table, self.engine, if_exists="append", index=False)
        except Exception as e:
            print(f"Error {e} occurred.")

    def update(self):
        pass


class Graph:
    @staticmethod
    def graph(x, y, lbl="data"):
        plt.plot(x, y, label=lbl)

    @staticmethod
    def show():
        plt.show()
