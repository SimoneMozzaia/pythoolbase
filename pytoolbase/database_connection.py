import os.path
import jaydebeapi as jdb
import logging
import pandas as pd
from .configuration_file import Configuration
from .my_logger import CustomLogger


class Database:
    __instance = None
    __config_class = None
    __path_man_class = None
    __custom_logger = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__call__(*args, **kwargs)
        return cls.__instance

    def __init__(self, path_manipulation_class):
        self.__config_class = Configuration()
        self.__custom_logger = CustomLogger('DatabaseClass').custom_logger(logging.INFO)
        self.__path_man_class = path_manipulation_class
        self.__custom_logger.info(f'Initializing Database Class. Parameter: {path_manipulation_class}')

    def connect_to_database(self, environment, country):
        self.__custom_logger.info(f"connect_to_database. Parameters: {environment}, {country}")

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
    __path_class = None

    def __init__(self, path_manipulation_class):
        self.__config_class = Configuration()
        self.__custom_logger = CustomLogger('QueriesClass').custom_logger(logging.INFO)
        self.__path_class = path_manipulation_class
        self.__custom_logger.info(f'Initializing Queries Class')

    def get_pandas_df_from_query(self, query_file, connection, parameters):
        """Returns a pandas dataframe generated from an SQL query.

        Args:
             query_file (str): Name of the .sql file to be executed
             connection (connection):   Connection to the database
             parameters (dict): Dictionary contains sql query parameters. Can be None

        Returns:
            A pandas dataframe
        """
        self.__custom_logger.info(f'get_pandas_df_from_query. Parameters {query_file}, {connection}, {parameters}')

        query_path = self.__path_class.get_queries_path()
        query_to_execute = os.path.join(query_path, query_file)

        with open(query_to_execute) as f:
            self.__custom_logger.debug(f"Get sql script from file {query_to_execute} with parameters {parameters}")
            sql = f.read()
            self.__custom_logger.debug(f"Query: {sql}")

        self.__custom_logger.debug("Created pandas dataframe")

        if parameters is not None:
            return pd.read_sql(sql, connection, params=parameters)
        else:
            return pd.read_sql(sql, connection)
