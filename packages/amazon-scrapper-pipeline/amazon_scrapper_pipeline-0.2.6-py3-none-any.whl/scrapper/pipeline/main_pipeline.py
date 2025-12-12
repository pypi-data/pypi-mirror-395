import os
import sys
from pathlib import Path
from datetime import datetime


# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from scrapper.entity.config_entity import DataConfig 
from scrapper.entity.artifact_entity import UrlDataArtifact, ProductDataArtifact
from scrapper.src.multi_url_scrapper import AmazonUrlScraper
from scrapper.src.multi_product_scrapper import AmazonProductScraper
from scrapper.logger import GLOBAL_LOGGER as log
from scrapper.exception.custom_exception import CustomException



class AmazonScrapingPipeline:
    """
    Orchestrates the complete Amazon scraping pipeline:
    1. URL Scraping - Collects product URLs from search results
    2. Product Scraping - Extracts detailed information from each product page
    
    Artifacts are saved in timestamped directories:
    - Artifacts/<timestamp>/UrlData/urls.json
    - Artifacts/<timestamp>/ProductData/products.json
    """
    
    def __init__(
        self,
        search_terms: list[str] | str,
        target_links: int | list[int] = 5,
        headless: bool = False,
        return_url_data: bool = False,  # ← Added
        return_prod_data: bool = False  # ← Added
    ):
        """
        Initialize the scraping pipeline.
        
        Args:
            search_terms: Single term or list of product search terms
            target_links: Number of URLs to scrape per term (int or list)
            headless: Run browsers in headless mode (default: False)
            return_url_data: Return URL data along with artifact (default: False)
            return_prod_data: Return product data along with artifact (default: False)
        """
        self.search_terms = search_terms
        self.target_links = target_links
        self.headless = headless
        self.return_url_data = return_url_data  # ← Store
        self.return_prod_data = return_prod_data  # ← Store
        
        # Pipeline artifacts
        self.data_config: DataConfig = None
        self.url_artifact: UrlDataArtifact = None
        self.product_artifact: ProductDataArtifact = None
        
        # In-memory data storage
        self.url_data: dict = None
        self.product_data: dict = None
    
    def _log_stage_header(self, stage_name: str, stage_number: int):
        """Log formatted stage header."""
        log.info(f"\n{'='*80}")
        log.info(f"STAGE {stage_number}: {stage_name}")
        log.info(f"{'='*80}\n")
    
    def _log_stage_complete(self, stage_name: str):
        """Log stage completion."""
        log.info(f"\n{'✓'*80}")
        log.info(f"✅ {stage_name} - COMPLETED")
        log.info(f"{'✓'*80}\n")
    
    def start_url_scraping(self) -> UrlDataArtifact | tuple[UrlDataArtifact, dict]:
        """
        Stage 1: Scrape product URLs from Amazon search results.
        
        Returns:
            UrlDataArtifact containing path to urls.json
            or (UrlDataArtifact, dict) when return_url_data is True
        """
        self._log_stage_header("URL SCRAPING", 1)
        
        try:
            # Initialize configuration with timestamp
            self.data_config = DataConfig(timestamp=datetime.now())
            
            log.info(f"📂 Artifact directory: {self.data_config.SAVED_DATA_DIR}")
            log.info(f"🔍 Search terms: {self.search_terms}")
            log.info(f"🎯 Target links: {self.target_links}")
            log.info(f"👁️ Headless mode: {self.headless}")
            log.info(f"📊 Return URL data: {self.return_url_data}\n")
            
            # Initialize URL scraper
            url_scraper = AmazonUrlScraper(
                data_config=self.data_config,
                search_terms=self.search_terms,
                target_links=self.target_links,
                headless=self.headless,
                wait_timeout=5,
                page_load_timeout=15,
                return_url_data=self.return_url_data  # ← Pass flag
            )
            
            # Run URL scraping
            result = url_scraper.run()
            
            # Unpack based on return_url_data flag
            if self.return_url_data:
                self.url_artifact, self.url_data = result
            else:
                self.url_artifact = result
                self.url_data = None
            
            log.info(f"✅ URLs saved to: {self.url_artifact.url_file_path}")
            
            # Enhanced logging if data available
            if self.url_data:
                log.info(f"📊 URLs collected: {self.url_data.get('total_urls', 0)} across {self.url_data.get('total_products', 0)} categories")
            
            self._log_stage_complete("URL SCRAPING")
            
            # Return based on flag
            if self.return_url_data:
                return self.url_artifact, self.url_data
            return self.url_artifact
            
        except Exception as e:
            log.error("❌ URL scraping stage failed", exc_info=True)
            raise CustomException(e, sys)
    
    def start_product_scraping(self) -> ProductDataArtifact | tuple[ProductDataArtifact, dict]:
        """
        Stage 2: Scrape detailed product information from collected URLs.
        
        Returns:
            ProductDataArtifact containing path to products.json and statistics
            or (ProductDataArtifact, dict) when return_prod_data is True
        """
        self._log_stage_header("PRODUCT SCRAPING", 2)
        
        try:
            if not self.url_artifact:
                raise ValueError("URL artifact not found. Run start_url_scraping() first.")
            
            log.info(f"📂 Loading URLs from: {self.url_artifact.url_file_path}")
            log.info(f"👁️ Headless mode: {self.headless}")
            log.info(f"📊 Return product data: {self.return_prod_data}\n")
            
            # Initialize product scraper
            product_scraper = AmazonProductScraper(
                data_config=self.data_config,
                url_data_artifact=self.url_artifact,
                headless=self.headless,
                wait_timeout=10,
                page_load_timeout=20,
                return_prod_data=self.return_prod_data  # ← Pass flag
            )
            
            # Run product scraping
            result = product_scraper.run()
            
            # Unpack based on return_prod_data flag
            if self.return_prod_data:
                self.product_artifact, self.product_data = result
            else:
                self.product_artifact = result
                self.product_data = None
            
            log.info(f"✅ Products saved to: {self.product_artifact.product_file_path}")
            
            # Enhanced logging if data available
            if self.product_data:
                log.info(f"📊 Products scraped: {self.product_data.get('total_scraped', 0)}, Failed: {self.product_data.get('total_failed', 0)}")
            
            self._log_stage_complete("PRODUCT SCRAPING")
            
            # Return based on flag
            if self.return_prod_data:
                return self.product_artifact, self.product_data
            return self.product_artifact
            
        except Exception as e:
            log.error("❌ Product scraping stage failed", exc_info=True)
            raise CustomException(e, sys)
    
    def run_pipeline(self) -> tuple[UrlDataArtifact, ProductDataArtifact] | tuple[UrlDataArtifact, dict, ProductDataArtifact, dict]:
        """
        Execute the complete pipeline: URL scraping → Product scraping.
        
        Returns:
            If both return flags are False: (UrlDataArtifact, ProductDataArtifact)
            If return_url_data=True only: (UrlDataArtifact, dict, ProductDataArtifact)
            If return_prod_data=True only: (UrlDataArtifact, ProductDataArtifact, dict)
            If both True: (UrlDataArtifact, dict, ProductDataArtifact, dict)
        """
        try:
            log.info(f"\n{'#'*80}")
            log.info(f"🚀 STARTING AMAZON SCRAPING PIPELINE")
            log.info(f"{'#'*80}\n")
            
            pipeline_start = datetime.now()
            
            # Stage 1: URL Scraping
            url_result = self.start_url_scraping()
            
            # Stage 2: Product Scraping
            product_result = self.start_product_scraping()
            
            # Pipeline completion summary
            pipeline_end = datetime.now()
            duration = (pipeline_end - pipeline_start).total_seconds()
            
            self._log_pipeline_summary(duration)
            
            # Return based on flags
            if self.return_url_data and self.return_prod_data:
                return self.url_artifact, self.url_data, self.product_artifact, self.product_data
            elif self.return_url_data:
                return self.url_artifact, self.url_data, self.product_artifact
            elif self.return_prod_data:
                return self.url_artifact, self.product_artifact, self.product_data
            else:
                return self.url_artifact, self.product_artifact
            
        except Exception as e:
            log.error("❌ Pipeline execution failed", exc_info=True)
            raise CustomException(e, sys)
    
    def _log_pipeline_summary(self, duration: float):
        """Log pipeline execution summary."""
        log.info(f"\n{'#'*80}")
        log.info(f"🎉 PIPELINE COMPLETED SUCCESSFULLY")
        log.info(f"{'#'*80}")
        log.info(f"\n📊 PIPELINE SUMMARY:")
        log.info(f"├── Timestamp: {self.data_config.timestamp}")
        log.info(f"├── Duration: {duration:.2f} seconds")
        log.info(f"├── URLs file: {self.url_artifact.url_file_path}")
        log.info(f"└── Products file: {self.product_artifact.product_file_path}")
        
        # URL data summary if available
        if self.url_data:
            log.info(f"\n📈 URL DATA SUMMARY:")
            log.info(f"├── Total products: {self.url_data.get('total_products', 0)}")
            log.info(f"├── Total URLs: {self.url_data.get('total_urls', 0)}")
            log.info(f"└── Categories:")
            for product, info in self.url_data.get('products', {}).items():
                log.info(f"    ├── {product}: {info['count']} URLs")
        
        # Product scraping statistics
        if hasattr(self.product_artifact, 'scraped_count'):
            log.info(f"\n📈 SCRAPING STATISTICS:")
            log.info(f"├── Successfully scraped: {self.product_artifact.scraped_count}")
            log.info(f"├── Failed: {self.product_artifact.failed_count}")
            total = self.product_artifact.scraped_count + self.product_artifact.failed_count
            success_rate = (self.product_artifact.scraped_count / total * 100) if total > 0 else 0
            log.info(f"└── Success rate: {success_rate:.2f}%")
        
        # Product data summary if available
        if self.product_data:
            log.info(f"\n📦 PRODUCT DATA SUMMARY:")
            log.info(f"├── Total scraped: {self.product_data.get('total_scraped', 0)}")
            log.info(f"├── Total failed: {self.product_data.get('total_failed', 0)}")
            log.info(f"└── Categories:")
            for category, products in self.product_data.get('products', {}).items():
                log.info(f"    ├── {category}: {len(products)} product(s)")
                # Show first product sample
                for product in products[:1]:
                    if product.get('Product Name'):
                        log.info(f"    │   ├── Sample: {product['Product Name'][:50]}...")
                    if product.get('Product Price'):
                        log.info(f"    │   └── Price: {product['Product Price']}")
        
        log.info(f"\n{'#'*80}\n")



# ==================== MAIN EXECUTION ====================


def main():
    """Main entry point for the pipeline."""
    try:
        # Configure pipeline parameters
        pipeline = AmazonScrapingPipeline(
            search_terms=['laptop pc'],
            target_links=1,  # 1 laptop, 2 mice
            headless=False,  # Set to False to see browser
            return_url_data=False,  # ← Get URL data in memory
            return_prod_data=True  # ← Get product data in memory
        )
        
        # Execute complete pipeline
        result = pipeline.run_pipeline()
        
        # Unpack result based on return flags
        if pipeline.return_url_data and pipeline.return_prod_data:
            url_artifact, url_data, product_artifact, product_data = result
            
            print(f"\n✅ Pipeline completed with full data!")
            print(f"📁 URLs: {url_artifact.url_file_path}")
            print(f"📁 Products: {product_artifact.product_file_path}")
            
            print(f"\n📊 URL Data:")
            print(f"  • Total URLs: {url_data['total_urls']}")
            print(f"  • Categories: {url_data['total_products']}")
            
            print(f"\n📦 Product Data:")
            print(f"  • Scraped: {product_data['total_scraped']}")
            print(f"  • Failed: {product_data['total_failed']}")
            
        elif pipeline.return_url_data:
            url_artifact, url_data, product_artifact = result
            
            print(f"\n✅ Pipeline completed with URL data!")
            print(f"📁 URLs: {url_artifact.url_file_path}")
            print(f"📁 Products: {product_artifact.product_file_path}")
            print(f"📊 Total URLs: {url_data['total_urls']}")
            
        elif pipeline.return_prod_data:
            url_artifact, product_artifact, product_data = result
            
            print(f"\n✅ Pipeline completed with product data!")
            print(f"📁 URLs: {url_artifact.url_file_path}")
            print(f"📁 Products: {product_artifact.product_file_path}")
            print(f"📦 Scraped: {product_data['total_scraped']}")
        else:
            url_artifact, product_artifact = result
            
            print(f"\n✅ Pipeline completed!")
            print(f"📁 URLs: {url_artifact.url_file_path}")
            print(f"📁 Products: {product_artifact.product_file_path}")
        
    except Exception as e:
        log.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)



if __name__ == "__main__":
    main()
