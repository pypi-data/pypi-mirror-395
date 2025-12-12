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
import json
import time
import os, sys



class AmazonUrlScraper:
    """
    Scrapes product URLs from Amazon search results and saves them to
    Artifacts/<timestamp>/UrlData/urls.json (per your configs).

    Notes:
      - Amazon’s bot detection is strict. This does NOT solve captchas.
      - If you encounter captchas, consider using a residential proxy service.
    """
    def __init__(
        self,
        data_config: DataConfig,
        search_term: str,
        target_links: int = 35,
        headless: bool = False,
        wait_timeout: int = 5,
        page_load_timeout: int = 15):
    
        # Configs
        self.data_config = data_config
        self.url_cfg = UrlDataConfig(data_config)
        self.search_term = search_term
        self.target_links = int(target_links)
        self.headless = bool(headless)
        self.wait_timeout = int(wait_timeout)
        self.page_load_timeout = int(page_load_timeout)

        # Base URL (strip trailing slash to avoid //)
        self.base_url = (BASE_URL or "https://www.amazon.in/").rstrip("/")

        # Ensure output dir exists
        self._ensure_output_dir()

        # Runtime
        self.driver = None
        self.wait = None
        self.urls: list[str] = []

    # ----------------- Setup/Teardown -----------------
    
    def _ensure_output_dir(self):
        # Create UrlData directory if missing
        os.makedirs(self.url_cfg.url_data_dir, exist_ok=True)
    
    def _build_options(self):
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

        return options
    
    def _start(self):
        try:
            options = self._build_options()
            self.driver = uc.Chrome(
                driver_executable_path=ChromeDriverManager().install(),
                options=options,
                use_subprocess=True,
            )
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, self.wait_timeout)
        except Exception as e:
            log.error("Failed to start Chrome driver", exc_info=True)
            raise CustomException(e, sys)
        
    
    def _quit(self):
        if self.driver:
            try:
                self.driver.close()  # Close first
                time.sleep(0.5)      # Small delay
                self.driver.quit()   # Then quit
            except:
                pass
            finally:
                self.driver = None
    
    def _wait_dom_ready(self):
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            log.debug(f'Page loaded: "{self.driver.title}"')
        except Exception:
            log.warning(f'Page may not be fully loaded: "{self.driver.title}"')


    def _clean_href(self, href: str) -> str | None:
        if not href:
            return None
        parsed_qs = parse_qs(urlparse(href).query)
        if "url" in parsed_qs:
            return self.base_url + unquote(parsed_qs["url"][0])
        return href if href.startswith("http") else self.base_url + href
    
    
    def _search(self):
        try:
            self.driver.get(self.base_url)
            self._wait_dom_ready()

            bar = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
            bar.clear()
            bar.send_keys(self.search_term)
            time.sleep(1.5)

            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-search-submit-button"]')))
            btn.click()
            self._wait_dom_ready()
        except Exception as e:
            log.error("Search initiation failed (DOM change or bot detection).", exc_info=True)
            raise CustomException(e, sys)
    
    def _collect_current_page(self):
        try: 
            # Find the next button element
            next_button = self.driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
            
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
        
        anchors = self.driver.find_elements(By.CLASS_NAME, "a-link-normal")
        added = 0
        for a in anchors:
            href = self._clean_href(a.get_attribute("href"))
            if not href:
                continue

            # If you want to restrict to product pages only, uncomment:
            if "/dp/" not in href and "/gp/product/" not in href:
                continue

            if href not in self.urls:
                self.urls.append(href)
                added += 1
                if len(self.urls) >= self.target_links:
                    break
        # log.debug(f"Collected {added} new links on this page.")
        log.debug(f"Collected {added} new links on this page. Total: {len(self.urls)}")
    
    def _next_page(self) -> bool:
        try:
            # nxt = self.driver.find_element(By.CSS_SELECTOR, ".s-pagination-next")
            # Use correct selector for Amazon's next button
            nxt = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.s-pagination-next"))
        )   
             # Check if next button is disabled (last page)
            if nxt.get_attribute("aria-disabled") == "true":
                log.info("Next button is disabled - reached last page")
                return False
            
            # Scroll to next button
            # self.driver.execute_script("arguments[0].scrollIntoView(true);", nxt)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", nxt)
            time.sleep(1.5)
            # self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-next"))).click() 
            self.driver.execute_script("arguments[0].click();", nxt)
            time.sleep(2)  # Wait for navigation
            self._wait_dom_ready()
            log.info("Successfully navigated to next page")
            return True
        except Exception as e:
            log.info(f"No next page or click failed: {e}")
            return False

    def _save(self):
        try:
            # save_json_file(self.urls, self.url_cfg.url_file_path)
            save_json_file(self.url_cfg.url_file_path, self.urls)
            log.info(f"Saved {len(self.urls)} URLs -> {self.url_cfg.url_file_path}")
        except Exception as e:
            log.error("Failed to save URL JSON.", exc_info=True)
            raise CustomException(e, sys)
    

            
    # ----------------- Public API -----------------
    def run(self) -> UrlDataArtifact:
        if not self.search_term or not self.search_term.strip():
            raise CustomException(ValueError("search_term is required."), sys)
        try:
            self._start()
            self._search()

            page = 0
            while len(self.urls) < self.target_links:
                page += 1
                time.sleep(2)
                self._collect_current_page()
                if len(self.urls) >= self.target_links:
                    break
                if not self._next_page():
                    log.info(f"Stopped after {page} page(s).")
                    break

            self._save()
            return UrlDataArtifact(url_file_path=self.url_cfg.url_file_path)

        except CustomException:
            raise
        except Exception as e:
            log.error("Unexpected error during scraping.", exc_info=True)
            raise CustomException(e, sys)
        finally:
            self._quit()


# ---- Example usage (remove in production) ----
if __name__ == "__main__":
    # Builds: Artifacts/<timestamp>/UrlData/urls.json
    dc = DataConfig()  # uses current timestamp by default
    scraper = AmazonUrlScraper(
        data_config=dc,
        search_term="32 inch Monitor 4k+",
        target_links=130,
        headless=False,
        wait_timeout=5,
        page_load_timeout=15,
    )
    artifact = scraper.run()
    print({"saved_to": artifact.url_file_path})
