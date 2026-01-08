import logging
import csv
from openpyxl.workbook import Workbook
from openpyxl.styles import Font
from openpyxl import load_workbook
import os
from shutil import copyfile
from .my_logger import CustomLogger
import xlwings as xw
from .configuration_file import Configuration
import formulas


class CustomFile:
    """Class to create and style custom files from SQL queries.

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
        db_class        Instance of the Database class. Used to get data from the database
    """
    __custom_logger = None
    __db_class = None
    __cfg_class = None

    def __init__(self):
        """At class initialization make sure that the working folder for temporary files
        exists. If not, it creates it
        """
        self.__custom_logger = CustomLogger('CustomFileClass').custom_logger(logging.DEBUG)
        self.__custom_logger.info(f'Initializing CustomFile Class')

        if not os.path.exists(r'.\working_files'):
            os.mkdir(r'.\working_files')

    def create_csv_file_from_pandas_dataframe(self, pandas_dataframe, csv_file_path):
        """Creates a csv file from a specific sql query.


        Args:
            pandas_dataframe (dataframe):   Pandas dataframe to be turned into a csv file
            csv_file_path (str):    Path of the csv file that has to be created

        Return:
            Nothing
        """
        self.__custom_logger.info(f"create_csv_file_from_pandas_dataframe. Parameters: {csv_file_path}")
        self.__custom_logger.debug(f"Dataframe {pandas_dataframe}.")
        
        pandas_dataframe.to_csv(
            csv_file_path
            , encoding='utf-8'
            , header=True
            , doublequote=True
            , sep=','
            , index=False
            , decimal='.'
        )
        self.__custom_logger.debug(f"Created csv file {csv_file_path}.")

    def create_excel_file_from_csv(self, csv_file_path, excel_file_path, encoding):
        self.__custom_logger.info(
            f"create_excel_file_from_csv. Parameters: {csv_file_path}, {excel_file_path}, {encoding}"
        )

        wb = Workbook()
        ws = wb.active

        with open(csv_file_path, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                ws.append(row)

        logging.debug("Style the file")
        ws.freeze_panes = ws['A2']
        ws.auto_filter.ref = ws.dimensions

        for row in ws.iter_rows():

            for cell in row:

                ws.column_dimensions[cell.column_letter].width = 25

                if cell.row == 1:
                    ws[cell.coordinate].font = Font(bold=True)

                # Cell formatting
                match cell.column_letter:

                    case _:
                        if cell.row > 1:
                            ws[cell.coordinate].number_format = '@'

        self.__custom_logger.info("Deleting the csv file")
        os.remove(csv_file_path)

        self.__custom_logger.info(f"Saving the excel file at {excel_file_path}")
        wb.save(excel_file_path)

        self.__custom_logger.info(f"Excel file created.")

    def copy_file_to_remote_folder(self, local_path, remote_path):
        """Use the copyfile utility to upload a local file to a remote folder

        Args:
            local_path  Path to the local file to be uploaded
            remote_path Path where to copy the local file
        """
        self.__custom_logger.info(f"copy_file_to_remote_folder. Parameters: {local_path}, {remote_path}")
        
        copyfile(local_path, remote_path)

    def get_column_values_for_each_row(self, excel_file_path, column_indexes):
        """

        Args:
            column_indexes (list):  List of column indexes to consider in the selection
            excel_file_path (str):  Path to the Excel file to open

        Returns:
            values_dict (dict): A dictionary containing relevant values
                                retrieved from specific columns
        """
        self.__custom_logger.info(f"get_column_values_for_each_row. Parameters: {excel_file_path}, {column_indexes}")

        workbook = load_workbook(excel_file_path)
        sheet = workbook['Sheet']
        values_dict = {}
        i = 0

        for row in sheet.iter_rows():
            value_list = []
            for cell in row:
                if cell.row != 1:
                    if cell.column in column_indexes:
                        value_list.append(cell.value.replace(' ', ''))

            if len(value_list) != 0:
                values_dict[i] = value_list

            i += 1

        return values_dict

    def save_calculated_cell_value(self, excel_file_to_update):
        """
        Given a specific cell value calculated with a formula,
        saves the value itself without the calculations.

        During the process the initial formula is lost
        """
        self.__custom_logger.info(
            f"save_calculated_cell_value. Parameters: {excel_file_to_update}"
        )

        # Save calculated results
        self.__custom_logger.info(f'Saving calculated results')
        xl_model = formulas.ExcelModel().loads(excel_file_to_update).finish()
        xl_model.calculate()
        xl_model.write(dirpath=r'.\external_files')


    def get_list_from_env_file(self, environment_file_path, key_to_extract):
        self.__custom_logger.info(
            f"get_list_from_env_file. Parameters: {environment_file_path}, {key_to_extract}"
        )
        self.__cfg_class = Configuration()

        env_file = self.__cfg_class.get_value_from_env_file(environment_file_path)
        values = env_file[key_to_extract]
        list_of_values = list(values)

        for val in list_of_values:
            if val == ',':
                list_of_values.remove(val)

        return list_of_values
