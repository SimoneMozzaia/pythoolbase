import os.path
import jaydebeapi as jdb
import pandas as pd
from .my_logger import CustomLogger


class Database:
    __instance = None
    __config_class = None
    __custom_logger = None
    __general_env_path = None
    __general_env_secrets = None
    __country_env_secrets = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__call__(*args, **kwargs)
        return cls.__instance

    def __init__(self, configuration_class):
        self.__config_class = configuration_class
        self.__custom_logger = CustomLogger('DatabaseClass').custom_logger(
            self.__config_class.get_log_level_from_log_key("database_class_log_level")
        )
        self.__general_env_secrets = self.__config_class.load_env_file()
        self.__custom_logger.info(
            f'Initializing Database Class. Parameters: {configuration_class}'
        )

    def connect_to_database(self, environment, country):
        self.__custom_logger.info(f"connect_to_database. Parameters: {environment}, {country}")

        country_env_secrets = self.__config_class.load_env_file(
            environment=environment,
            country=country
        )

        jdbc_driver = self.__general_env_secrets["jdbc_driver"]
        jdbc = self.__general_env_secrets["jdbc"]
        server = country_env_secrets["db_host"]
        user = country_env_secrets["db_user"]
        password = country_env_secrets["db_password"]

        # Example of connection to a DB2 server
        connection = jdb.connect(
            jdbc_driver,
            jdbc + server + ";prompt=false",
            [
                user
                , password
            ],
            self.__config_class.load_env_file()["jt400_jar_path"]
        )

        self.__custom_logger.debug(f"Established database connection {connection}.")

        return connection


class Queries:
    __custom_logger = None
    __config_class = None
    __query_path = None

    def __init__(self, configuration_class):
        self.__config_class = configuration_class
        self.__custom_logger = CustomLogger('QueriesClass').custom_logger(
            self.__config_class.get_log_level_from_log_key("queries_class_log_level")
        )
        self.__query_path = self.__config_class.get_queries_path()
        self.__custom_logger.info(
            f'Initializing Queries Class. Parameters: {configuration_class}'
        )

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

        query_to_execute = os.path.join(self.__query_path, query_file)

        with open(query_to_execute) as f:
            self.__custom_logger.info(f"Get sql script from file {query_to_execute} with parameters {parameters}")
            sql = f.read()
            self.__custom_logger.debug(f"Query: {sql}")

        self.__custom_logger.debug("Created pandas dataframe")

        if parameters is not None:
            return pd.read_sql(sql, connection, params=parameters)
        else:
            return pd.read_sql(sql, connection)

    def execute_insert(self, connection, query, params=None):
        self.__custom_logger.info(f'execute_insert. Parameters {query}, {connection}, {params}')
        cursor = connection.cursor()

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        cursor.close()
