from scrapper.exception.custom_exception import CustomException 
from pathlib import Path
import json
import yaml
import sys, os

def read_json_file(file_path: str) -> dict:
    """
    Reads a JSON file and returns its content as a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        raise CustomException(e, sys) from e
    
    
def save_json_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Saves content to a JSON file. If replace=True, it overwrites the existing file.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, indent=2, ensure_ascii=False)
    except Exception as e:
        raise CustomException(e, sys) from e


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    
    try:
        yaml_path = Path(file_path)
        
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        
        if not yaml_path.is_file():
            raise ValueError(f"Path is not a file: {yaml_path}")
        
        with open(yaml_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)
        
        if content is None:
            return {}
        
        return content
        
    except FileNotFoundError as e:
        raise CustomException(e, sys)

    except Exception as e:
        raise CustomException(e, sys)