import re
import os
import multiprocessing

from data_generator.utils.utility import get_data_path
from data_generator.database.tables import Logs
from data_generator.database.datawriter import DataWriter

class LogParser():
    def __init__(self) -> None:
        self.lines = []
        
    def __call__(self, log_file_path: str = os.path.join(get_data_path(), "Linux", "Linux.log")):
        data_writer = DataWriter()
        self.load_log = self.load_log(log_file_path)
        rows = self.parse_log()
        data_writer.write_multiple_rows_to_database(rows)
    
    def load_log(self, log_file_path: str = os.path.join(get_data_path(), "Linux", "Linux.log")):
        with open(log_file_path, "rb") as f:
            self.lines = f.readlines()
            
    def parse_log(self):
        with multiprocessing.Pool(processes=8) as pool:
            result = pool.map(self._split_log_message, self.lines)
        return [x for x in result if x is not None]
        
    @staticmethod
    def _split_log_message(log_message: str):
        pattern = re.compile(r"(\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2})\s+(.*)")
        try:
            match = pattern.match(log_message.decode('utf-8'))
            if match:
                time = match.group(1)
                message = match.group(2)
                return Logs(log_time=time, log_message=message)
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError: ", e)