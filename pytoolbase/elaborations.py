from pytoolbase.my_logger import CustomLogger
from datetime import datetime


class DataframeManipulations:
    __config_class = None
    __custom_logger = None
    __custom_file_class = None
    __env_file = None

    def __init__(self, config_class, custom_file_class):
        self.__config_class = config_class
        self.__custom_file_class = custom_file_class
        self.__custom_logger = CustomLogger('DataframeManipulationsClass').custom_logger(
            self.__config_class.get_log_level_from_log_key("dataframe_man_log_level")
        )
        self.__env_file = self.__config_class.load_env_file()
        self.__custom_logger.info(
            f'Initializing DataframeManipulations Class. Parameters: {config_class}, {custom_file_class}'
        )

    def create_text_to_send(self, pandas_dataframe_not_grouped, pandas_dataframe_grouped, remote_path):
        self.__custom_logger.info(
            f'create_text_to_send. Parameters: {pandas_dataframe_not_grouped}, {pandas_dataframe_grouped}, {remote_path}'
        )

        partial_text_one = self.__create_recap_text(
            pandas_dataframe_not_grouped,
            self.__env_file["partial_text_not_grouped"],
            self.__env_file["non_grouped_headers"].split(',')
        )
        partial_text_two = self.__create_recap_text(
            pandas_dataframe_grouped,
            self.__env_file["partial_text_grouped"],
            self.__env_file["grouped_headers"].split(',')
        )

        text_to_send = rf'''<b>{self.__env_file["teams_message_title"]}</b><br>
            Data: {datetime.now().strftime("%Y/%m/%d")}
            {partial_text_one}
            <br>
            Grouped:
            {partial_text_two}
            <br>
            {self.__env_file["teams_message_footer"]} {remote_path}'''

        return text_to_send

    def __create_recap_text(self, pandas_dataframe, partial_text, headers):
        self.__custom_logger.info('__create_recap_text_not_grouped')
        self.__custom_logger.debug(f'{pandas_dataframe}, {partial_text}, {headers}')

        partial_text = self.__dataframe_calculations(partial_text, pandas_dataframe, headers)

        return partial_text

    def __dataframe_calculations(self, partial_text, pandas_dataframe, headers):
        self.__custom_logger.info('__dataframe_calculations')

        assoluto_sum = 0

        for row in range(len(pandas_dataframe)):
            # Get the summary for each row to send to the Teams chat
            for head in headers:
                if head == 'assoluto':
                    assoluto_sum = assoluto_sum + pandas_dataframe[head].values[row]
                partial_text = partial_text + rf'<td>{pandas_dataframe[head].values[row]}</td>'

            partial_text = partial_text + '</tr>'

        partial_text = partial_text + rf'</table><br><b>Somma Assoluta:</b> {assoluto_sum}'

        return partial_text

    def get_parameters_list(self, excel_path, columns_to_get):
        self.__custom_logger.info(f'get_parameters_list. Parameters {excel_path}, {columns_to_get}')

        return self.__custom_file_class.get_column_values_for_each_row(excel_path, columns_to_get)