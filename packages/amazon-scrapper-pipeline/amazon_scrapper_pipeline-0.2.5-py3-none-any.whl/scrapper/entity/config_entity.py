from scrapper.constant.configuration import *
from datetime import datetime   
import os


class DataConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.SAVED_DATA_DIR: str = os.path.join(SAVED_DATA_DIR, timestamp)
        self.timestamp: str = timestamp
    

class UrlDataConfig:
    def __init__(self, data_config:DataConfig):
        self.url_data_dir: str = os.path.join(data_config.SAVED_DATA_DIR, URL_DATA_DIR)
        self.url_file_path: str =  os.path.join(self.url_data_dir, URL_FILE_NAME)
        
class ProductDataConfig:
    def __init__(self, data_config:DataConfig):
        self.product_data_dir: str = os.path.join(data_config.SAVED_DATA_DIR, PRODUCT_DATA_DIR)
        self.product_file_path: str =  os.path.join(self.product_data_dir, PRODUCT_FILE_NAME)

