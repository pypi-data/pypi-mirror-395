import os
from pathlib import Path
import sys


# Add the project root to the Python path for direct script execution
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs, unquote
from scrapper.constant.configuration import BASE_URL
from scrapper.exception.custom_exception import CustomException
from scrapper.logger import GLOBAL_LOGGER as log
from scrapper.utils.main_utils import save_json_file
from scrapper.entity.config_entity import DataConfig, UrlDataConfig
from scrapper.entity.artifact_entity import UrlDataArtifact 
from scrapper.entity.url_locator_entity import AmazonLocators
from selenium.common.exceptions import TimeoutException
import json
import time
import os, sys



class AmazonUrlScraper:
    """
    Scrapes product URLs from Amazon search results and saves them to
    Artifacts/<timestamp>/UrlData/urls.json (per your configs).


    Notes:
      - Amazon's bot detection is strict. This does NOT solve captchas.
      - If you encounter captchas, consider using a residential proxy service.
    """
    def __init__(
        self,
        data_config: DataConfig,
        search_terms: list[str] | str,  # Accept list or single string
        target_links: int | list[int] = 5,
        headless: bool = False,
        wait_timeout: int = 5,
        page_load_timeout: int = 15,
        locators_config_path: str = None,
        return_url_data: bool = False):
    
        # Configs
        self.data_config = data_config
        self.url_cfg = UrlDataConfig(data_config)
        
        # Normalize search_terms to list
        self.search_terms = [search_terms] if isinstance(search_terms, str) else search_terms
        
        # Normalize target_links
        if isinstance(target_links, int):
            # Apply same target to all products
            self.target_links_list = [target_links] * len(self.search_terms)
        else:
            # Use per-product targets
            if len(target_links) != len(self.search_terms):
                raise ValueError(
                    f"Length of target_links ({len(target_links)}) must match "
                    f"search_terms ({len(self.search_terms)})"
                )
            self.target_links_list = target_links
        
        self.headless = bool(headless)
        self.wait_timeout = int(wait_timeout)
        self.page_load_timeout = int(page_load_timeout)
        self.return_url_data = return_url_data
        
        # Base URL (strip trailing slash to avoid //)
        self.base_url = (BASE_URL or "https://www.amazon.in/").rstrip("/")


        # Load locators from YAML
        self.locators = AmazonLocators(locators_config_path)


        # Ensure output dir exists
        self._ensure_output_dir()


        # Runtime
        self.driver = None
        self.wait = None
        self.urls: list[str] = []
        self.all_results: dict[str, list[str]] = {}  # Store URLs per product
        self.current_target: int = 0  # Track current target for _collect_current_page


    # ----------------- Setup/Teardown -----------------
    def _ensure_output_dir(self):
        """Create UrlData directory if missing."""
        os.makedirs(self.url_cfg.url_data_dir, exist_ok=True)
    
    def _build_chrome_options(self):
        """Build Chrome options based on headless setting."""
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
        """Initialize Chrome driver with anti-detection measures."""
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
        """Close and quit the driver safely."""
        if self.driver:
            try:
                self.driver.close()  # Close first
                time.sleep(0.5)      # Small delay
                self.driver.quit()   # Then quit
            except:
                pass
            finally:
                self.driver = None
    
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
            # Reduce wait time for bot detection check to avoid delays
            short_wait = WebDriverWait(self.driver, 3)
            continue_btn = short_wait.until(
                EC.element_to_be_clickable(self.locators.continue_button.as_tuple())
            )
            continue_btn.click()
            time.sleep(2)
            log.info("✓ Bot detection handled - clicked continue button")
            return True
        except TimeoutException:
            # Button not present - this is normal behavior
            return False
        except Exception as e:
            log.debug(f"Bot detection check failed: {e}")
            return False


    def _clean_href(self, href: str) -> str | None:
        """Clean and normalize product URLs."""
        if not href:
            return None
        parsed_qs = parse_qs(urlparse(href).query)
        if "url" in parsed_qs:
            return self.base_url + unquote(parsed_qs["url"][0])
        return href if href.startswith("http") else self.base_url + href
    
    def _search(self, search_term: str):
        """Perform search for a specific term."""
        try:
            self.driver.get(self.base_url)
            self._wait_for_page_load()
            
            # Check for bot detection after initial page load
            if self._handle_bot_detection():
                self._wait_for_page_load()
           
            # Use locator from config
            bar = self.wait.until(
                EC.presence_of_element_located(self.locators.search_box.as_tuple())
            )
            bar.clear()
            bar.send_keys(search_term)
            time.sleep(1.5)
            
            # Use locator from config
            btn = self.wait.until(
                EC.element_to_be_clickable(self.locators.search_button.as_tuple())
            )
            btn.click()
            self._wait_for_page_load()
            
            # Check for bot detection after search results load
            if self._handle_bot_detection():
                self._wait_for_page_load()
            
            log.info(f"Search completed for: '{search_term}'")
            
        except Exception as e:
            log.error(f"Search failed for '{search_term}'", exc_info=True)
            raise CustomException(e, sys)
    
    def _collect_current_page(self):
        """Collect product URLs from current page."""
        try: 
            # Find the next button element and scroll to it
            next_button = self.driver.find_element(*self.locators.next_button.as_tuple())
            
            # Scroll to next button to ensure all products above it are loaded
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", 
                next_button
            )
            time.sleep(1.5)  # Wait for lazy-loaded content
        except:
            # If next button not found, scroll to bottom (last page)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
        
        # Use locator from config
        anchors = self.driver.find_elements(*self.locators.product_link.as_tuple())
        added = 0
        
        for a in anchors:
            href = self._clean_href(a.get_attribute("href"))
            if not href:
                continue


            # Restrict to product pages only
            if "/dp/" not in href and "/gp/product/" not in href:
                continue


            if href not in self.urls:
                self.urls.append(href)
                added += 1
                if len(self.urls) >= self.current_target:
                    break
        
        log.debug(f"Collected {added} new links on this page. Total: {len(self.urls)}")
    
    def _next_page(self) -> bool:
        """Navigate to next page of search results."""
        try:
            # Use locator from config
            nxt = self.wait.until(
                EC.presence_of_element_located(self.locators.next_button.as_tuple())
            )   
            
            # Check if next button is disabled (last page)
            if nxt.get_attribute("aria-disabled") == "true":
                log.info("Next button is disabled - reached last page")
                return False
            
            # Scroll to next button
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                nxt
            )
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", nxt)
            time.sleep(2)  # Wait for navigation
            self._wait_for_page_load()
            
            # Check for bot detection after pagination
            if self._handle_bot_detection():
                self._wait_for_page_load()
            
            log.info("Successfully navigated to next page")
            return True
            
        except Exception as e:
            log.info(f"No next page or click failed: {e}")
            return False


    def _save(self):
        """Save all collected URLs organized by search term with counts."""
        try:
            # Prepare final payload with counts
            final_payload = {
                "total_products": len(self.all_results),
                "total_urls": sum(len(urls) for urls in self.all_results.values()),
                "products": {}
            }
            
            # Add each product with its URL count
            for search_term, urls in self.all_results.items():
                final_payload["products"][search_term] = {
                    "count": len(urls),
                    "urls": urls
                }
            
            # Save to JSON
            save_json_file(self.url_cfg.url_file_path, final_payload)
            
            total = final_payload["total_urls"]
            log.info(f"Saved {total} URLs across {len(self.all_results)} products -> {self.url_cfg.url_file_path}")
            
            return final_payload
        
        except Exception as e:
            log.error("Failed to save URL JSON.", exc_info=True)
            raise CustomException(e, sys)


    # ----------------- Public API -----------------
    def run(self) -> UrlDataArtifact | tuple[UrlDataArtifact, dict]:
        """
        Main execution method to scrape URLs for all search terms.


        Returns:
            UrlDataArtifact
            or (UrlDataArtifact, dict) when self.return_url_data is True
        """
        if not self.search_terms:
            raise CustomException(ValueError("At least one search_term is required."), sys)
        
        try:
            self._initialize_driver()
            
            # Iterate over search terms with their corresponding targets
            for search_term, target in zip(self.search_terms, self.target_links_list):
                log.info(f"Scraping '{search_term}' (target: {target} links)")
                self.urls = []  # Reset for each product
                self.current_target = target  # Set current target
                
                self._search(search_term)
                
                page = 0
                while len(self.urls) < target:
                    page += 1
                    time.sleep(2)
                    self._collect_current_page()
                    
                    if len(self.urls) >= target:
                        break
                        
                    if not self._next_page():
                        log.info(f"Stopped after {page} page(s) for '{search_term}'")
                        break
                
                self.all_results[search_term] = self.urls[:target]
                log.info(f"Collected {len(self.urls)} URLs for '{search_term}'")
            
            payload = self._save()  # returns the dict
            artifact = UrlDataArtifact(url_file_path=self.url_cfg.url_file_path)



            if self.return_url_data:
                log.info(f"✅ RETURNING TUPLE: (artifact, payload)")
                return_value = (artifact, payload)
                log.info(f"🔍 return_value type = {type(return_value)}")
                log.info(f"🔍 return_value length = {len(return_value) if isinstance(return_value, tuple) else 'N/A'}")
                return return_value
            else:
                log.info(f"✅ RETURNING ARTIFACT ONLY")
                return artifact
        
        except CustomException:
            raise
        except Exception as e:
            log.error("Unexpected error during scraping.", exc_info=True)
            raise CustomException(e, sys)
        finally:
            self._close_driver()
