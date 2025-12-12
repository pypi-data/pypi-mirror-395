import os
import sys
from pathlib import Path
from datetime import datetime


# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from scrapper.entity.config_entity import DataConfig 
from scrapper.entity.artifact_entity import UrlDataArtifact
from scrapper.src.multi_url_scrapper import AmazonUrlScraper
from scrapper.logger import GLOBAL_LOGGER as log
from scrapper.exception.custom_exception import CustomException
from typing import Union, Tuple


class AmazonUrlScrapingPipeline:
    """
    URL Scraping Pipeline: Collects product URLs from Amazon search results.

    Artifacts are saved in timestamped directories:
    - Artifacts/<timestamp>/UrlData/urls.json
    """

    def __init__(
        self,
        search_terms: list[str] | str,
        target_links: int | list[int] = 5,
        headless: bool = False,
        wait_timeout: int = 5,
        page_load_timeout: int = 15,
        return_url_data: bool = False
    ):
        """
        Initialize the URL scraping pipeline.

        Args:
            search_terms: Single term or list of product search terms
            target_links: Number of URLs to scrape per term (int or list)
            headless: Run browsers in headless mode (default: False)
            wait_timeout: Element wait timeout in seconds (default: 5)
            page_load_timeout: Page load timeout in seconds (default: 15)
            return_url_data: Return scraped data along with artifact (default: False)
        """
        self.search_terms = search_terms
        self.target_links = target_links
        self.headless = headless
        self.wait_timeout = wait_timeout
        self.page_load_timeout = page_load_timeout
        self.return_url_data = return_url_data

        # Pipeline artifacts
        self.data_config: DataConfig = None
        self.url_artifact: UrlDataArtifact = None

    def _log_stage_header(self, stage_name: str):
        """Log formatted stage header."""
        log.info(f"\n{'='*80}")
        log.info(f"{stage_name}")
        log.info(f"{'='*80}\n")

    def _log_stage_complete(self, stage_name: str):
        """Log stage completion."""
        log.info(f"\n{'✓'*80}")
        log.info(f"✅ {stage_name} - COMPLETED")
        log.info(f"{'✓'*80}\n")

    def run(self) -> UrlDataArtifact | tuple[UrlDataArtifact, dict]:
        """
        Execute URL scraping pipeline.

        Returns:
            UrlDataArtifact containing path to urls.json
            or (UrlDataArtifact, dict) when self.return_url_data is True
        """
        self._log_stage_header("🚀 AMAZON URL SCRAPING PIPELINE")

        try:
            pipeline_start = datetime.now()

            # Initialize configuration with timestamp
            self.data_config = DataConfig(timestamp=pipeline_start)

            log.info(f"📂 Artifact directory: {self.data_config.SAVED_DATA_DIR}")
            log.info(f"🔍 Search terms: {self.search_terms}")
            log.info(f"🎯 Target links: {self.target_links}")
            log.info(f"👁️ Headless mode: {self.headless}")
            log.info(f"⏱️ Wait timeout: {self.wait_timeout}s")
            log.info(f"⏱️ Page load timeout: {self.page_load_timeout}s")
            log.info(f"📊 Return data: {self.return_url_data}\n")

            # Initialize URL scraper
            url_scraper = AmazonUrlScraper(
                data_config=self.data_config,
                search_terms=self.search_terms,
                target_links=self.target_links,
                headless=self.headless,
                wait_timeout=self.wait_timeout,
                page_load_timeout=self.page_load_timeout,
                return_url_data=self.return_url_data
            )

            # Run URL scraping
            result = url_scraper.run()
            # Unpack result based on return_url_data setting
            if self.return_url_data:
                self.url_artifact, scraped_data = result  # ← Unpack tuple
            else:
                self.url_artifact = result  # ← Assign artifact directly
                scraped_data = None


            # Calculate duration
            pipeline_end = datetime.now()
            duration = (pipeline_end - pipeline_start).total_seconds()

            # Log summary
            self._log_pipeline_summary(duration, scraped_data)

            if self.return_url_data:
                return self.url_artifact, scraped_data
            return self.url_artifact


        except Exception as e:
            log.error("❌ URL scraping pipeline failed", exc_info=True)
            raise CustomException(e, sys)

    def _log_pipeline_summary(self, duration: float, data: dict | None = None):
        """
        Log pipeline execution summary.
        
        Args:
            duration: Pipeline execution time in seconds
            data: Optional scraped data dictionary for enhanced logging
        """
        log.info(f"\n{'#'*80}")
        log.info(f"🎉 URL SCRAPING PIPELINE COMPLETED")
        log.info(f"{'#'*80}")
        log.info(f"\n📊 PIPELINE SUMMARY:")
        log.info(f"├── Timestamp: {self.data_config.timestamp}")
        log.info(f"├── Duration: {duration:.2f} seconds")
        log.info(f"└── URLs file: {self.url_artifact.url_file_path}")
        
        # Enhanced logging when data is available
        if data:
            log.info(f"\n📈 SCRAPED DATA SUMMARY:")
            log.info(f"├── Total products: {data.get('total_products', 0)}")
            log.info(f"├── Total URLs: {data.get('total_urls', 0)}")
            log.info(f"└── Products:")
            for product, info in data.get('products', {}).items():
                log.info(f"    ├── {product}: {info['count']} URLs")
        
        log.info(f"\n{'#'*80}\n")


# ==================== MAIN EXECUTION ====================


def main():
    """Main entry point for the URL scraping pipeline."""
    try:
        # Configure pipeline parameters
        pipeline = AmazonUrlScrapingPipeline(
            search_terms=['laptop pc'],
            target_links=1,  # 1 laptop, 2 mice
            headless=True,  # Set to True to hide browser
            wait_timeout=5,
            page_load_timeout=15,
            return_url_data = False 
        )

        # Execute pipeline
        result = pipeline.run()
        if pipeline.return_url_data:
            url_artifact, scraped_data = result

            print(scraped_data)
            print(f"\n✅ URL scraping completed with data!")
            print(f"📁 URLs saved to: {url_artifact.url_file_path}")
            print(f"\n📊 In-memory data:")
            print(f"   Total products: {scraped_data['total_products']}")
            print(f"   Total URLs: {scraped_data['total_urls']}")
            print(f"\n   Products breakdown:")
            for product, info in scraped_data['products'].items():
                print(f"   - {product}: {info['count']} URLs")
                for i, url in enumerate(info['urls'][:3], 1):  # Show first 3
                    print(f"     {i}. {url[:80]}...")
            
        else:
            url_artifact = result
            
            print(f"\n✅ URL scraping completed!")
            print(f"📁 URLs saved to: {url_artifact.url_file_path}")
            print(f"\n💡 Use this file path in the Product Scraping Pipeline")

    except Exception as e:
        log.error(f"URL scraping pipeline failed: {e}", exc_info=True)
        sys.exit(1)



if __name__ == "__main__":
    main()
