import os
from pathlib import Path
import sys
import json
import time
import random


# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager


from scrapper.exception.custom_exception import CustomException
from scrapper.logger import GLOBAL_LOGGER as log
from scrapper.utils.main_utils import save_json_file, read_json_file
from scrapper.entity.config_entity import DataConfig, ProductDataConfig
from scrapper.entity.artifact_entity import UrlDataArtifact, ProductDataArtifact
from scrapper.entity.product_locator_entity import AmazonLocators



class AmazonProductScraper:
    """
    Scrapes individual product details from Amazon product pages.
    
    Loads URLs from UrlDataArtifact, scrapes each product page, and saves
    ALL products to a single JSON file: products.json
    
    Uses YAML-based locators for easier maintenance.
    """
    
    def __init__(
        self,
        data_config: DataConfig,
        url_data_artifact: UrlDataArtifact,
        headless: bool = False,
        wait_timeout: int = 10,
        page_load_timeout: int = 20,
        return_prod_data: bool = False
    ):
        """
        Initialize the Amazon Product Scraper.
        
        Args:
            data_config: Configuration for artifact paths
            url_data_artifact: Artifact containing URL file path from URL scraper
            headless: Run Chrome in headless mode (default: False)
            wait_timeout: Explicit wait timeout in seconds (default: 10)
            page_load_timeout: Page load timeout in seconds (default: 20)
            return_prod_data: Return scraped data along with artifact (default: False)
        """
        # Configuration
        self.data_config = data_config
        self.url_data_artifact = url_data_artifact
        self.product_cfg = ProductDataConfig(data_config)
        
        # Settings
        self.headless = bool(headless)
        self.wait_timeout = int(wait_timeout)
        self.page_load_timeout = int(page_load_timeout)
        self.return_prod_data = return_prod_data 
        
        # Load locators from YAML
        self.locators = AmazonLocators()
        
        # Runtime state
        self.driver = None
        self.wait = None
        self.urls_data: dict[str, list[str]] = {}
        self.products_data: dict[str, list[dict]] = {}
        self.scraped_count = 0
        self.failed_count = 0
        
        # Ensure output directory exists
        self._ensure_output_dir()
    
    # ==================== Setup & Teardown ====================
    
    def _ensure_output_dir(self):
        """Create ProductData directory if it doesn't exist."""
        os.makedirs(self.product_cfg.product_data_dir, exist_ok=True)
        log.info(f"✓ Product data directory: {self.product_cfg.product_data_dir}")
    
    def _build_chrome_options(self) -> uc.ChromeOptions:
        """Build Chrome options with anti-detection measures."""
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-features=NetworkServiceInProcess")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,900")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-browser-side-navigation")
        
        return options
    
    def _initialize_driver(self):
        """Initialize Chrome driver with anti-detection scripts."""
        try:
            options = self._build_chrome_options()
            
            self.driver = uc.Chrome(
                driver_executable_path=ChromeDriverManager().install(),
                options=options,
                use_subprocess=True,
            )
            
            self.driver.set_page_load_timeout(self.page_load_timeout)
            
            # Anti-detection: Override user agent via CDP
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # Anti-detection: Hide webdriver property
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)
            
            if not self.headless:
                self.driver.maximize_window()
            
            self.wait = WebDriverWait(self.driver, self.wait_timeout)
            log.info("✓ Chrome driver initialized successfully")
            
        except Exception as e:
            log.error("Failed to initialize Chrome driver", exc_info=True)
            raise CustomException(e, sys)
    
    def _close_driver(self):
        """Safely close and quit Chrome driver."""
        if self.driver:
            try:
                self.driver.close()
                time.sleep(0.5)
                self.driver.quit()
                log.info("✓ Chrome driver closed")
            except Exception as e:
                log.warning(f"Error closing driver: {e}")
            finally:
                self.driver = None
                self.wait = None
    
    # ==================== Helper Methods ====================
    
    def _scroll_to_element(self, element):
        """Scroll element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
    
    def _wait_for_page_load(self):
        """Wait for page to fully load."""
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            log.debug(f'Page loaded: "{self.driver.title}"')
        except Exception:
            log.warning(f'Page may not be fully loaded: "{self.driver.title}"')
    
    def _handle_bot_detection(self):
        """Handle Amazon anti-bot 'Continue shopping' button if it appears."""
        try:
            # Use shorter wait time to avoid delays when button is not present
            short_wait = WebDriverWait(self.driver, 3)
            continue_btn = short_wait.until(
                EC.element_to_be_clickable(self.locators.continue_button.as_tuple())
            )
            continue_btn.click()
            time.sleep(2)
            log.info("✓ Bot detection handled - clicked continue button")
            return True
        except TimeoutException:
            # Button not present - this is normal
            return False
        except Exception as e:
            log.debug(f"Bot detection check failed: {e}")
            return False
  
    def _load_urls_from_artifact(self):
        """Load URLs from the UrlDataArtifact JSON file."""
        try:
            data = read_json_file(self.url_data_artifact.url_file_path)
            
            # Extract products from new structure
            if "products" in data:
                # New format with counts
                self.urls_data = {
                    product: details["urls"] 
                    for product, details in data["products"].items()
                }
                total = data.get("total_urls", sum(len(urls) for urls in self.urls_data.values()))
                num_products = data.get("total_products", len(self.urls_data))
            else:
                # Old format (backward compatibility)
                self.urls_data = data
                total = sum(len(urls) for urls in self.urls_data.values())
                num_products = len(self.urls_data)
            
            log.info(f"✓ Loaded {total} URLs from {num_products} categories")
            
        except Exception as e:
            log.error("Failed to load URLs from artifact", exc_info=True)
            raise CustomException(e, sys)


    
    # ==================== Scraping Method with YAML Locators ====================
    
    def _scrape_product(self, url: str, category: str) -> dict:
        """
        Scrapes a single Amazon product page using YAML-based locators.
        
        Args:
            url: Product URL to scrape
            category: Category/search term for this product
            
        Returns:
            dict: Product data
        """
        self.driver.get(url)
        self._wait_for_page_load()
        
        # Check for bot detection after page load
        if self._handle_bot_detection():
            self._wait_for_page_load()
        
        time.sleep(random.uniform(2, 4))
        
        data = {
            "Product URL": url,
            "Category": category
        }
        
        # Main container
        rows = self.driver.find_elements(*self.locators.main_container.as_tuple())
        
        for row in rows:
            
            # Product Name
            try:
                name = row.find_element(*self.locators.product_title.as_tuple())
                self._scroll_to_element(name)
                data["Product Name"] = name.text.strip()
            except:
                data["Product Name"] = None
            
            # Price
            try:
                price = row.find_element(*self.locators.product_price.as_tuple())
                self._scroll_to_element(price)
                data["Product Price"] = price.text.strip()
            except:
                data["Product Price"] = None
            
            # Ratings
            try:
                ratings = row.find_element(*self.locators.ratings.as_tuple())
                self._scroll_to_element(ratings)
                data["Ratings"] = ratings.text.strip()
            except:
                data["Ratings"] = None
            
            # Total Reviews
            try:
                total_reviews = row.find_element(*self.locators.total_reviews.as_tuple())
                self._scroll_to_element(total_reviews)
                data["Total Reviews"] = total_reviews.text.strip()
            except:
                data["Total Reviews"] = None
            
            # About this item
            try:
                about_item = row.find_element(*self.locators.about_item.as_tuple())
                self._scroll_to_element(about_item)
                data["About this item"] = about_item.text.strip()
            except:
                data["About this item"] = None
            
            # Technical Details
            tech_details = {}
            try:
                table = self.wait.until(
                    EC.presence_of_element_located(self.locators.tech_details_table.as_tuple())
                )
                self._scroll_to_element(table)
                
                for tr in table.find_elements(*self.locators.tech_details_row.as_tuple()):
                    try:
                        k = tr.find_element(*self.locators.tech_details_key.as_tuple()).text.strip()
                        v = tr.find_element(*self.locators.tech_details_value.as_tuple()).text.strip()
                        if k:
                            tech_details[k] = v
                    except:
                        continue
                
                data["Technical Details"] = tech_details
                
            except:
                data["Technical Details"] = None
        
        # CUSTOMER REVIEWS
        review_cards = self.driver.find_elements(*self.locators.review_cards.as_tuple())
        reviews_list = []
        
        for card in review_cards:
            self._scroll_to_element(card)
            
            try:
                name = card.find_element(*self.locators.reviewer_name.as_tuple()).text.strip()
            except:
                name = None
            
            try:
                body = card.find_element(*self.locators.review_text_content.as_tuple()).text.strip()
            except:
                try:
                    body = card.find_element(*self.locators.review_text.as_tuple()).text.strip()
                except:
                    body = None
            
            reviews_list.append({
                "Customer Name": name,
                "Customer Review": body
            })
        
        data["Customer Reviews"] = reviews_list
        
        return data
    
    # ==================== Public API ====================
    
    def run(self) -> ProductDataArtifact | tuple[ProductDataArtifact, dict]:
        """
        Main scraping workflow - loads URLs, scrapes all products, saves to single JSON.
        
        Returns:
            ProductDataArtifact with file path and statistics
            or (ProductDataArtifact, dict) when self.return_prod_data is True
        """
        try:
            # Step 1: Load URLs from artifact
            self._load_urls_from_artifact()
            
            if not self.urls_data:
                raise ValueError("No URLs found in artifact file")
            
            # Step 2: Initialize Chrome driver
            self._initialize_driver()
            
            # Initialize products data structure
            self.products_data = {category: [] for category in self.urls_data.keys()}
            
            # Calculate total URLs to scrape
            total_urls = sum(len(urls) for urls in self.urls_data.values())
            current_count = 0
            
            log.info(f"\n{'='*70}")
            log.info(f"Starting Amazon Product Scraping")
            log.info(f"Total products to scrape: {total_urls}")
            log.info(f"Categories: {len(self.urls_data)}")
            log.info(f"{'='*70}\n")
            
            # Step 3: Iterate through categories and URLs
            for category, urls in self.urls_data.items():
                log.info(f"\n{'='*70}")
                log.info(f"📦 Category: {category}")
                log.info(f"Products: {len(urls)}")
                log.info(f"{'='*70}\n")
                
                for idx, url in enumerate(urls, 1):
                    current_count += 1
                    log.info(f"[{current_count}/{total_urls}] Scraping product {idx}/{len(urls)}...")
                    
                    try:
                        # Scrape the product using YAML-based locators
                        product_data = self._scrape_product(url, category)
                        
                        # Add to category list
                        self.products_data[category].append(product_data)
                        
                        # Increment success counter
                        self.scraped_count += 1
                        
                        log.info(f"✓ Scraped: {product_data.get('Product Name', 'Unknown')[:50]}")
                        
                    except Exception as e:
                        log.error(f"❌ Failed to process {url}: {e}")
                        # Add error entry
                        self.products_data[category].append({"url": url, "error": str(e)})
                        self.failed_count += 1
                        continue
                    
                    # Random delay between products
                    delay = random.uniform(2, 4)
                    time.sleep(delay)
            
            # Step 4: Save all products to single JSON file
            final_payload = {
                "total_scraped": self.scraped_count,
                "total_failed": self.failed_count,
                "products": self.products_data
            }
            
            save_json_file(self.product_cfg.product_file_path, final_payload)
            
            # Step 5: Summary
            log.info(f"\n{'='*70}")
            log.info(f"✅ Scraping Completed!")
            log.info(f"{'='*70}")
            log.info(f"✓ Successfully scraped: {self.scraped_count} products")
            log.info(f"✗ Failed: {self.failed_count} products")
            log.info(f"📁 Saved to: {self.product_cfg.product_file_path}")
            log.info(f"{'='*70}\n")
            
            #  Return based on return_prod_data flag
            artifact = ProductDataArtifact(
                product_data_dir=self.product_cfg.product_data_dir,
                product_file_path=self.product_cfg.product_file_path,
                scraped_count=self.scraped_count,
                failed_count=self.failed_count
            )
            if self.return_prod_data:
                return artifact, final_payload
            return artifact
            
        except CustomException:
            raise
        except Exception as e:
            log.error("Unexpected error during product scraping", exc_info=True)
            raise CustomException(e, sys)
        finally:
            self._close_driver()
