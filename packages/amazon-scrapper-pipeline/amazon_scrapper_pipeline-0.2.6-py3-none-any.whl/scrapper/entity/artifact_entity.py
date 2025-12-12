from dataclasses import dataclass

@dataclass
class DataArtifact:
    file_path: str


@dataclass
class UrlDataArtifact:
    url_file_path: str
    # raw_data_file_path: str

@dataclass
class ProductDataArtifact:
    product_file_path: str
    product_data_dir: str = None
    scraped_count: int = 0
    failed_count: int = 0