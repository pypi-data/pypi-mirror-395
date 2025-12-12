from brynq_sdk_brynq import BrynQ
import json
import os
import pandas as pd
import pymysql
import warnings
from datetime import datetime
from typing import Union, List, Optional, Literal


class MySQL(BrynQ):

    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, return_queries: bool = False, debug=False):
        """
        This class is used for connecting to a mysql database
        :param label: the label of the connection
        :param debug: if true, the queries will be printed
        """
        # This is built in so you can use this class as a query generator for the BrynQ Agent
        super().__init__()
        self.debug = debug
        self.return_queries = return_queries
        if return_queries:
            print("Running in query return mode")
        else:
            try:
                credentials = self.interfaces.credentials.get(system="mysql", system_type=system_type)
                credentials = credentials.get('data')
                self.host = credentials['host']
                self.user = credentials['username']
                self.password = credentials['password']
                self.database = credentials['schema']
                self.port = 3306 if credentials['port'] is None else int(credentials['port'])
            except Exception as e:
                if self.debug:
                    print("No credentials found in the platform for MySQL, defaulting to environment variables")
                self.host = None
            if self.host is None:
                if os.getenv("MYSQL_HOST") is not None:
                    self.host = os.getenv("MYSQL_HOST") if self.environment == 'prod' else os.getenv("MYSQL_STAGING_HOST")
                    self.user = os.getenv("MYSQL_USER")
                    self.password = os.getenv("MYSQL_PASSWORD")
                    self.database = os.getenv("MYSQL_DATABASE")
                    self.port = 3306 if os.getenv("MYSQL_PORT") is None else int(os.getenv("MYSQL_PORT"))
                else:
                    raise ValueError("No credentials found for MySQL, set MYSQL env variables or connect mysql authorization to your interface")

    def raw_query(self, query, insert=False) -> Optional[Union[list, str]]:
        """
        This method is used for sending queries to a mysql database
        :param query: the query to send
        :param insert: if true, the query will be executed as an insert
        :return:
        """
        if self.debug:
            print(query)
        if self.return_queries:
            return query
        else:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            cursor = connection.cursor()
            cursor.execute(query)
            if insert:
                connection.commit()
                connection.close()
            else:
                data = cursor.fetchall()
                connection.close()

                return list(data)

    def update(self, table: str, columns: List, values: List, filter='') -> Optional[str]:
        """
        This method is used for updating a mysql database
        :param table: the table to update
        :param columns: the columns to update
        :param values: the values to update
        :param filter: filter that selects the rows to update
        :return: message with the number of updated rows
        """
        update_values = ''

        def __map_strings(item):
            if isinstance(item, str):
                return '"' + str(item) + '"'
            elif isinstance(item, datetime):
                return '"' + item.strftime("%Y-%m-%d %H:%M:%S") + '"'
            else:
                return str(item)

        for index in range(len(columns)):
            if index != len(columns) - 1:
                update_values += "`{}` = {},".format(columns[index], __map_strings(values[index]))
            else:
                update_values += "`{}` = {}".format(columns[index], __map_strings(values[index]))
        update_values = update_values.replace('None', 'DEFAULT')
        query = "UPDATE {} SET {} {};".format(table, update_values, filter)
        if self.debug:
            print(query)
        if self.return_queries:
            return query
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        resp = cursor.execute(query)
        connection.commit()
        connection.close()

        return f"Updated {resp} rows in {table}"

    def select_metadata(self, table: str) -> List:
        """
        This method is used for getting the metadata of a table
        :param table: the table to get the metadata from
        :return: the columns of the table
        """
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        cursor.arraysize = 1
        query = f"SELECT COLUMN_NAME FROM `information_schema`.`COLUMNS` WHERE `TABLE_NAME` = '{table}' AND `TABLE_SCHEMA` =  '{self.database}' ORDER BY `ORDINAL_POSITION`"
        if self.debug:
            print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        # convert tuples to list
        data = [column[0] for column in data]

        return data

    def select(self, table: str, selection: str, filter='') -> Union[List, str]:
        query = f"SELECT {selection} FROM {table} {filter}"
        if self.debug:
            print(query)
        if self.return_queries:
            return query
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        cursor.arraysize = 10000
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()

        return list(data)

    def insert(self, table: str, dataframe: pd.DataFrame = None, ignore_duplicates=False, on_duplicate_key_update_columns: list = None, data: [pd.DataFrame, dict, list] = None, columns: list = None):
        if dataframe is not None:
            data = dataframe
            warnings.warn("dataframe parameter is vervangen door data parameter", DeprecationWarning)

        def __map_strings(item):
            return "'" + str(item).replace("'", "''") + "'" if isinstance(item, str) else str(item)

        if isinstance(data, dict):
            table_headers = ', '.join(data.keys())
            values = ','.join(map(__map_strings, data.values()))
        elif isinstance(data, pd.DataFrame):
            table_headers = ", ".join(list(data))
            data = data.where(pd.notnull(dataframe), None).copy()
            data = data.reset_index(drop=True)

            # build tuples with our safe mapper
            # Replace NA datatypes with None, which can be understood by the db as null/default
            values = ",".join(
                "(" + ",".join(__map_strings(v) for v in row) + ")"
                for row in data.itertuples(index=False, name=None)
            ).replace("None", "DEFAULT")
        elif isinstance(data, list):
            if columns is None:
                raise Exception('Columns parameter should be present when data is of type list')
            table_headers = ', '.join(columns)
            values = ','.join(map(__map_strings, data))

        # build the query, different scenario's and datatypes require different logic
        if ignore_duplicates:
            query = f"""INSERT IGNORE INTO {table} ({table_headers}) VALUES {values}""" if isinstance(data, pd.DataFrame) else f"""INSERT IGNORE INTO {table} ({table_headers}) VALUES ({values})"""
        elif on_duplicate_key_update_columns is not None:
            on_duplicate_key_update_columns = ', '.join([f'{column} = VALUES({column})' for column in on_duplicate_key_update_columns])
            query = f"""INSERT INTO {table} ({table_headers}) VALUES {values} ON DUPLICATE KEY UPDATE {on_duplicate_key_update_columns}""" if isinstance(data, pd.DataFrame) else f"""INSERT INTO {table} ({table_headers}) VALUES ({values}) ON DUPLICATE KEY UPDATE {on_duplicate_key_update_columns}"""
        else:
            query = f"""INSERT INTO {table} ({table_headers}) VALUES {values}""" if isinstance(data, pd.DataFrame) else f"""INSERT INTO {table} ({table_headers}) VALUES ({values})"""

        if self.debug:
            print(query)
        if self.return_queries:
            return query

        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        resp = cursor.execute(query)
        connection.commit()
        connection.close()

        return f'Inserted {resp} rows into {table}'

    def delete(self, table, filter='') -> str:
        query = f"DELETE FROM {table} {filter}"
        if self.debug:
            print(query)
        if self.return_queries:
            return query
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        resp = cursor.execute(query)
        connection.commit()
        connection.close()

        return f'Deleted {resp} rows from {table}'

    def create_table_if_not_exists(self, table, dataframe):
        # Map dataframe datatypes to monetdb datatypes. First in set is dataframe type, second is monetdb.
        datatypes = [
            {'dataframe_type': 'int64', 'mysql_type': 'INT'},
            {'dataframe_type': 'uint64', 'mysql_type': 'VARCHAR(255)'},
            {'dataframe_type': 'object', 'mysql_type': 'VARCHAR(255)'},
            {'dataframe_type': 'float64', 'mysql_type': 'FLOAT'},
            {'dataframe_type': 'datetime64[ns]', 'mysql_type': 'TIMESTAMP'},
            {'dataframe_type': 'bool', 'mysql_type': 'BOOLEAN'}
        ]
        datatypes = pd.DataFrame(datatypes)

        # Create a dataframe with all the types of the given dataframe
        dataframe_types = pd.DataFrame({'columns': dataframe.dtypes.index, 'types': dataframe.dtypes.values})
        dataframe_types = dataframe_types.to_json()
        dataframe_types = json.loads(dataframe_types)
        dataframe_types_columns = []
        dataframe_types_types = []

        for field in dataframe_types['columns']:
            dataframe_types_columns.append(dataframe_types['columns'][field])

        for type in dataframe_types['types']:
            dataframe_types_types.append(dataframe_types['types'][type]['name'])

        dataframe_types = pd.DataFrame({'columns': dataframe_types_columns, 'dataframe_type': dataframe_types_types})
        columns = pd.merge(dataframe_types, datatypes, on='dataframe_type', how='left')
        headers = ''
        for index, row in columns.iterrows():
            value = '`' + row['columns'] + '` ' + row['mysql_type']
            headers += ''.join(value) + ', '
        headers = headers[:-2]
        query = f"CREATE TABLE IF NOT EXISTS {table} ({headers});"
        if self.debug:
            print(query)
        if self.return_queries:
            return query

        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        resp = cursor.execute(query)
        connection.commit()
        connection.close()

        return f'Updated {resp} new table in database'

    def drop_table(self, table) -> str:
        query = f"DROP TABLE IF EXISTS {table}"
        if self.debug:
            print(query)
        if self.return_queries:
            return query

        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        resp = cursor.execute(query)
        connection.commit()
        connection.close()

        return f'Dropped {resp} table from database'

    def ping(self):
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        connection.ping()
