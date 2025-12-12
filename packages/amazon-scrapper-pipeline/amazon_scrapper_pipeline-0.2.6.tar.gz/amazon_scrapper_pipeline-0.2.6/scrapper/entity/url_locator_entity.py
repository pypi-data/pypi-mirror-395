from dataclasses import dataclass
from typing import Dict, Any
from pathlib import Path
from selenium.webdriver.common.by import By
from scrapper.utils.main_utils import read_yaml_file
import sys
from scrapper.logger import GLOBAL_LOGGER as log
from scrapper.exception.custom_exception import CustomException


@dataclass
class LocatorConfig:
    """Represents a single locator configuration."""
    by: str
    value: str
    
    VALID_BY_TYPES = {
        "ID": By.ID,
        "XPATH": By.XPATH,
        "CLASS_NAME": By.CLASS_NAME,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT
    }
    
    def get_by_type(self):
        """Convert string to By type with validation."""
        by_type_upper = self.by.upper()
        
        if by_type_upper not in self.VALID_BY_TYPES:
            valid_types = ", ".join(self.VALID_BY_TYPES.keys())
            raise ValueError(
                f"Invalid locator type: '{self.by}'. "
                f"Valid types are: {valid_types}"
            )
        
        return self.VALID_BY_TYPES[by_type_upper]
    
    def as_tuple(self):
        """Return as (By, value) tuple for Selenium."""
        return (self.get_by_type(), self.value)

class AmazonLocators:
    """Loads and provides access to Amazon locators from YAML."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "urls_locators.yaml"
        
        self.config_path = Path(config_path)
        self._load_locators()
    
    def _load_locators(self):
        """Load locators from YAML file using the utility function."""
        try:
            data = read_yaml_file(self.config_path)
            
            amazon_config = data.get('amazon_selectors', {})
            
            # Search locators
            search = amazon_config.get('search', {})
            self.search_box = LocatorConfig(**search.get('search_box', {}))
            self.search_button = LocatorConfig(**search.get('search_button', {}))
            
            # Results locators
            results = amazon_config.get('results', {})
            self.product_link = LocatorConfig(**results.get('product_link', {}))
            self.next_button = LocatorConfig(**results.get('next_button', {}))
            
            # Bot detection locators
            bot = amazon_config.get('bot_detection', {})
            self.continue_button = LocatorConfig(**bot.get('continue_button', {}))
            
            log.info("Amazon locators loaded successfully")
            
        except Exception as e:
            log.error("Failed to load Amazon locators", exc_info=True)
            raise CustomException(e, sys)
