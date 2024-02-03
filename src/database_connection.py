import jaydebeapi as jdb
import logging
import pandas as pd
import os
from .configuration_file import Configuration
from .path_manipulation import PathManipulation


class Database:
    __instance = None
    __config_class = None
    __path_man_class = None
    __custom_logger = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__call__(*args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__config_class = Configuration()
        self.__custom_logger = logging.getLogger(__name__)
        self.__path_man_class = PathManipulation()

    def connect_to_database(self, environment):
        self.__custom_logger.info(f"Application entered in module {__name__}.")

        user_pw_json_path = os.path.join(self.__path_man_class.get_secrets_path('secrets'), 'secrets.json')
        conn_files_json_path = os.path.join(self.__path_man_class.get_secrets_path('secrets'), 'env_paths.json')
        jar_path = os.path.join(self.__path_man_class.get_external_files_path('external_files'), 'jt400-11.1.jar')

        server_env = environment + '_host'
        user_env = environment + '_user'

        jdbc_driver = self.__config_class.get_value_from_json(conn_files_json_path, "db_connection_files",
                                                              "jdbc_driver")
        jdbc = self.__config_class.get_value_from_json(conn_files_json_path, "db_connection_files", "jdbc")
        server = self.__config_class.get_value_from_json(conn_files_json_path, "db_connection_server", server_env)

        user = self.__config_class.get_value_from_json(user_pw_json_path, "db_connection_user", user_env)
        password = self.__config_class.get_value_from_json(user_pw_json_path, "db_connection_password", "password")

        # Example of connection to a DB2 server
        connection = jdb.connect(
            jdbc_driver
            , jdbc
              + server
              + ";prompt=false"
            , [
                user
                , password
            ]
            , jar_path
        )

        self.__custom_logger.debug(f"Established database connection {connection}.")

        return connection


class Queries:
    __custom_logger = None

    def __init__(self):
        self.__custom_logger = logging.getLogger(__name__)

    def get_pandas_df_from_query(self, query_path, connection):
        """Returns a pandas dataframe generated from an SQL query.

        Args:
             query_path (str): Path to the query file
             connection (connection):   Connection to the database

        Returns:
            A pandas dataframe
        """
        with open(query_path) as f:
            self.__custom_logger.debug(f"Get sql script from file {query_path}")
            sql = f.read()
            self.__custom_logger.debug(f"Query: {sql}")

        self.__custom_logger.debug("Created pandas dataframe")

        return pd.read_sql(sql, connection)
