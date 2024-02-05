import jaydebeapi as jdb
import logging
import pandas as pd
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

    def connect_to_database(self, environment, country):
        self.__custom_logger.info(f"Application entered in module {__name__}.")
        jar_path = r'.\external_files\jt400-11.1.jar'

        country_env_path = self.__path_man_class.get_country_env_file(
                                            environment=environment,
                                            country=country)
        country_env_secrets = self.__config_class.get_value_from_env_file(country_env_path)
        general_env_path = self.__path_man_class.get_general_env_file()
        general_env_secrets = self.__config_class.get_value_from_env_file(general_env_path)

        jdbc_driver = general_env_secrets["jdbc_driver"]
        jdbc = general_env_secrets["jdbc"]
        server = country_env_secrets["db_host"]
        user = country_env_secrets["db_user"]
        password = country_env_secrets["db_password"]

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
