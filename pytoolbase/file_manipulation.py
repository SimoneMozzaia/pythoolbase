import logging
import csv
from openpyxl.workbook import Workbook
from openpyxl.styles import Font
import os
from shutil import copyfile
from .my_logger import CustomLogger


class CustomFile:
    """Class to create and style custom files from SQL queries.

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
        db_class        Instance of the Database class. Used to get data from the database
    """
    __custom_logger = None
    __db_class = None

    def __init__(self):
        self.__custom_logger = CustomLogger('CustomFileClass').custom_logger(logging.WARNING)

    def create_csv_file_from_pandas_dataframe(self, pandas_dataframe, csv_file_path):
        """Creates a csv file from a specific sql query.


        Args:
            pandas_dataframe (dataframe):   Pandas dataframe to be turned into a csv file
            csv_file_path (str):    Path of the csv file that has to be created

        Return:
            Nothing
        """
        self.__custom_logger.info("Create csv file")
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

    def create_excel_file_from_csv(self, csv_file_path, excel_file_path):
        self.__custom_logger.info("Create excel file")

        wb = Workbook()
        ws = wb.active

        with open(csv_file_path) as f:
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

        self.__custom_logger.debug("Delete the csv file")
        os.remove(csv_file_path)

        self.__custom_logger.debug(f"Saving excel file at {excel_file_path}")
        wb.save(excel_file_path)

        self.__custom_logger.info(f"Operations completed. Closing app.")

    def copy_file_to_remote_folder(self, local_path, remote_path):
        """Use the copyfile utility to upload a local file to a remote folder

        Args:
            local_path  Path to the local file to be uploaded
            remote_path Path where to copy the local file
        """
        self.__custom_logger.info(f"copy_file_to_remote_folder")
        
        copyfile(local_path, remote_path)
