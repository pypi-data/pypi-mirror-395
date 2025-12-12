# Amazon Scraper Pipelines


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)


Production-ready, Selenium-based pipelines for scraping Amazon search results and product details with a powerful FastAPI web interface.


## 🚀 Features


- ✅ **Modular Design**: URL and product scraping pipelines can be run independently or together
- ✅ **FastAPI REST API**: Full-featured API for programmatic access to all scraping pipelines
- ✅ **Beautiful Web UI**: Browser-based interface for running scrapers without writing code
- ✅ **Configurable Scraping**: Control search terms, number of URLs per term, timeouts, and headless mode
- ✅ **Timestamped Artifacts**: All outputs stored under timestamped folders for easy versioning
- ✅ **YAML-based Locators**: Page locators externalized into YAML for easier maintenance
- ✅ **Detailed Logging**: Structured logs for each stage and overall pipeline execution
- ✅ **In-memory Data Access**: Optionally return scraped data as Python dicts in addition to JSON files
- ✅ **Download API**: Download scraped data via REST endpoints


---


## 📦 Installation


```bash
pip install amazon-scraper-pipelines
```


### Requirements


- Python 3.8+
- Chrome/Chromium browser (for Selenium)


**Dependencies:**
```bash
pip install fastapi uvicorn selenium webdriver-manager pydantic jinja2 python-multipart pyyaml
```


---


## 🎯 Quick Start


### 🚀 Running the FastAPI Server


You can start the server in several ways depending on your workflow.

**Option 1: Run main.py directly (if uvicorn.run is inside)**

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "scrapper.router.api:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
```

```bash
python main.py
```

**Option 2: Use uvicorn from command line**

```bash
uvicorn scrapper.router.api:app --host 127.0.0.1 --port 8080
```

**Option 3: Development mode with auto-reload (recommended during development)**

```bash
uvicorn scrapper.router.api:app --host 127.0.0.1 --port 8080 --reload
```

**Option 4: Run on all network interfaces**

```bash
uvicorn scrapper.router.api:app --host 0.0.0.0 --port 8080
```

**Understanding the uvicorn command:**
- `scrapper.router.api:app` → The `app` object inside `scrapper/router/api.py` file (`app = FastAPI()`)
- `--host 127.0.0.1` → Binds to localhost only (most secure for local development)
- `--port 8080` → Server listens on port 8080
- `--reload` → Auto-reloads server when code changes (development only, NOT for production)
- `--host 0.0.0.0` → Makes server accessible from other machines on your network

**Server will be available at:**
- 🌐 **Web UI**: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
- 📚 **API Docs (Swagger)**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- 📖 **API Docs (ReDoc)**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)
---

### Using the Web Interface

1. Open [http://127.0.0.1:8080/](http://127.0.0.1:8080/) in your browser
2. Choose a scraper tab (Main Scraper / URL Scraper / Product Scraper)
3. Configure your scraping options
4. Click "Start Scraping"
5. Download results when complete

---

### Using Python Directly


```python
from scrapper.pipeline.main_pipeline import AmazonScrapingPipeline


# Run full pipeline: Search → URLs → Products
pipeline = AmazonScrapingPipeline(
    search_terms=['laptop', 'wireless mouse'],
    target_links=5,
    headless=True,
    return_url_data=True,
    return_prod_data=True
)


# Returns in this fixed order
url_artifact, url_data, product_artifact, product_data = pipeline.run_pipeline()


print(f"✅ URLs saved to: {url_artifact.url_file_path}")
print(f"✅ Products saved to: {product_artifact.product_file_path}")
print(f"📊 Total URLs: {url_data['total_urls']}")
print(f"📊 Scraped products: {product_data['total_scraped']}")
```


---
## ⚙️ Anti‑bot & network tips

For best results when running the scrapers:

1. **Use a fast and stable internet connection**  
   High latency or frequent disconnects can cause timeouts, incomplete loads, and more frequent bot challenges.

2. **Set `headless=False` while debugging**  
   Run the browser in visible mode during development to see what the scraper is doing, inspect page behavior, and understand where it fails.

3. **Use a VPN or proxy if you frequently see CAPTCHAs**  
   Switch to a different region or IP (respecting all legal and platform terms) when Amazon starts showing CAPTCHAs too often.

4. **Extend the code to handle bot detection for your use case**  
   The project is open for customization: adjust delays, headers, proxies, and Selenium behavior, and add your own strategies to better handle bot detection and anti-scraping defenses.

---

## 🌐 FastAPI Web Interface


The web interface provides three scraping modes accessible via tabs:


### 1. Main Scraper (Full Pipeline)
Runs both URL and Product scraping in sequence.


- **Search Terms**: Enter one search term per line
- **Target Links**: Number of product URLs to scrape per search term
- **Headless Mode**: Run browser without visible window
- **Return URL Data**: Include scraped URLs in API response
- **Return Product Data**: Include scraped product details in API response


### 2. URL Scraper
Collects only product URLs from Amazon search results.


- Outputs a JSON file with URLs organized by search term
- Useful when you want to review URLs before scraping product details


### 3. Product Scraper
Scrapes detailed product information from a previously generated URL file.


- Upload a `urls.json` file from a previous URL scrape
- Extracts price, specifications, reviews, and more


---


## 🔌 REST API Endpoints


### Health Check


```http
GET /api
```


**Response:**
```json
{
  "message": "Amazon Scraper Router API is running.",
  "version": "1.0.0"
}
```


---


### Main Scraper (Full Pipeline)


```http
POST /api/mainscrape
Content-Type: application/json
```


**Request Body:**
```json
{
  "search_terms": ["laptop", "wireless mouse"],
  "target_links": 5,
  "headless": true,
  "return_url_data": true,
  "return_prod_data": true
}
```


**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_terms` | `list[str]` | required | List of Amazon search terms |
| `target_links` | `int` | `list[int]` | required | URLs to scrape per term |
| `headless` | `bool` | `true` | Run browser in headless mode |
| `return_url_data` | `bool` | `false` | Include URL data in response |
| `return_prod_data` | `bool` | `false` | Include product data in response |


**Response (with both return flags true):**
```json
{
  "status": "success",
  "url_artifact": {
    "url_file_path": "Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
    "download_url": "/api/download/url-data/12_04_2025_14_58_45"
  },
  "product_artifact": {
    "product_file_path": "Artifacts/12_04_2025_14_58_45/ProductData/products.json",
    "download_url": "/api/download/product-data/12_04_2025_14_58_45"
  },
  "url_data": {
    "total_products": 2,
    "total_urls": 10,
    "products": {
      "laptop": {
        "count": 5,
        "urls": ["https://www.amazon.in/..."]
      }
    }
  },
  "product_data": {
    "total_scraped": 10,
    "total_failed": 0,
    "products": {
      "laptop": [
        {
          "Product Name": "...",
          "Product Price": "₹49,999",
          "Ratings": "4.5",
          "Technical Details": {},
          "Customer Reviews": []
        }
      ]
    }
  }
}
```


---


### URL Scraper


```http
POST /api/urlscrape
Content-Type: application/json
```


**Request Body:**
```json
{
  "search_terms": ["laptop"],
  "target_links": 10,
  "headless": true,
  "return_url_data": true
}
```


**Response:**
```json
{
  "status": "success",
  "url_artifact": {
    "url_file_path": "Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
    "download_url": "/api/download/url-data/12_04_2025_14_58_45"
  },
  "url_data": {
    "total_products": 1,
    "total_urls": 10,
    "products": {
      "laptop": {
        "count": 10,
        "urls": [
          "https://www.amazon.in/...",
          "https://www.amazon.in/..."
        ]
      }
    }
  }
}
```


---


### Product Scraper


```http
POST /api/productscrape
Content-Type: multipart/form-data
```


**Form Data:**
| Field | Type | Description |
|-------|------|-------------|
| `file` | `File` | JSON file containing URLs |
| `headless` | `bool` | Run browser in headless mode |
| `return_prod_data` | `bool` | Include product data in response |


**Example using cURL:**
```bash
curl -X POST "http://127.0.0.1:8080/api/productscrape" \
  -F "file=@urls.json" \
  -F "headless=true" \
  -F "return_prod_data=true"
```


**Response:**
```json
{
  "status": "success",
  "url_file_path": "Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
  "url_artifact": {
    "url_file_path": "...",
    "download_url": "/api/download/file?path=..."
  },
  "product_artifact": {
    "product_file_path": "Artifacts/12_04_2025_14_58_45/ProductData/products.json",
    "download_url": "/api/download/product-data/12_04_2025_14_58_45"
  },
  "product_data": {
    "total_scraped": 10,
    "total_failed": 0,
    "products": {}
  }
}
```


---


### Download Endpoints


**Download URL data by timestamp:**
```http
GET /api/download/url-data/{timestamp}
# Example: GET /api/download/url-data/12_04_2025_14_58_45
```


**Download product data by timestamp:**
```http
GET /api/download/product-data/{timestamp}
# Example: GET /api/download/product-data/12_04_2025_14_58_45
```


**Download by file path:**
```http
GET /api/download/file?path=Artifacts/12_04_2025_14_58_45/UrlData/urls.json
```


---


### Results Endpoints


**Get results by timestamp:**
```http
GET /api/results/{timestamp}
```


**List all available results:**
```http
GET /api/results
```


**Response:**
```json
{
  "results": [
    {
      "timestamp": "12_04_2025_14_58_45",
      "files": {
        "url_file": "Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
        "product_file": "Artifacts/12_04_2025_14_58_45/ProductData/products.json"
      },
      "download_urls": {
        "url_data": "/api/download/url-data/12_04_2025_14_58_45",
        "product_data": "/api/download/product-data/12_04_2025_14_58_45"
      }
    }
  ]
}
```


---


## 🐍 Python API


### 1. URL Scraping Pipeline


Collects product URLs from Amazon search results and saves them to a JSON file.


```python
from scrapper.pipeline.url_pipeline import AmazonUrlScrapingPipeline


pipeline = AmazonUrlScrapingPipeline(
    search_terms=['laptop pc', 'wireless mouse'],
    target_links=[5, 3],  # 5 laptops, 3 mice
    headless=True,
    return_url_data=True
)


url_artifact, url_data = pipeline.run()


print(f"URLs saved to: {url_artifact.url_file_path}")
print(f"Total URLs: {url_data['total_urls']}")
```


**Parameters:**
- `search_terms`: `list[str] | str` - Amazon search terms
- `target_links`: `int | list[int]` - URLs to scrape per term (default: 5)
- `headless`: `bool` - Run browser in headless mode (default: False)
- `wait_timeout`: `int` - Element wait timeout in seconds (default: 5)
- `page_load_timeout`: `int` - Page load timeout in seconds (default: 15)
- `return_url_data`: `bool` - Return URL data in memory (default: False)


**Returns:**
- When `return_url_data=False`: `(UrlDataArtifact,)`
- When `return_url_data=True`: `(UrlDataArtifact, dict)`


---


### 2. Product Scraping Pipeline


Reads a URL JSON file and scrapes detailed information for each product URL.


```python
from scrapper.pipeline.prodcut_pipeline import AmazonProductScrapingPipeline


pipeline = AmazonProductScrapingPipeline(
    url_file_path="Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
    headless=True,
    return_prod_data=True
)


product_artifact, product_data = pipeline.run()


print(f"Products saved to: {product_artifact.product_file_path}")
print(f"Success: {product_artifact.scraped_count}")
print(f"Failed: {product_artifact.failed_count}")
```


**Parameters:**
- `url_file_path`: `str | Path` - Path to URL JSON file (required)
- `headless`: `bool` - Run browser in headless mode (default: False)
- `wait_timeout`: `int` - Element wait timeout in seconds (default: 10)
- `page_load_timeout`: `int` - Page load timeout in seconds (default: 20)
- `return_prod_data`: `bool` - Return product data in memory (default: False)


**Returns:**
- When `return_prod_data=False`: `(ProductDataArtifact,)`
- When `return_prod_data=True`: `(ProductDataArtifact, dict)`


---


### 3. End-to-End Pipeline (Main)


Runs both URL and product scraping in sequence: **Search → URLs → Products**


```python
from scrapper.pipeline.main_pipeline import AmazonScrapingPipeline


pipeline = AmazonScrapingPipeline(
    search_terms=['laptop', 'wireless mouse'],
    target_links=[5, 3],
    headless=True,
    return_url_data=True,
    return_prod_data=True
)


# ALWAYS returns in this fixed order
url_artifact, url_data, product_artifact, product_data = pipeline.run_pipeline()


print(f"✅ URLs: {url_data['total_urls']}")
print(f"✅ Products: {product_data['total_scraped']}")
```


**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_terms` | `list[str]` | str | required | Amazon search terms |
| `target_links` | `int` | list[int] | 5 | URLs per search term |
| `headless` | `bool` | False | Run in headless mode |
| `wait_timeout` | `int` | 5 | Wait timeout (seconds) |
| `page_load_timeout` | `int` | 15 | Page load timeout (seconds) |
| `return_url_data` | `bool` | False | Return URL data in memory |
| `return_prod_data` | `bool` | False | Return product data in memory |


**Return Value (Fixed Order):**


```python
url_artifact, url_data, product_artifact, product_data = pipeline.run_pipeline()
```


| Variable | Type | Description |
|----------|------|-------------|
| `url_artifact` | `UrlDataArtifact` | Contains `url_file_path` |
| `url_data` | `dict` | None | URL data if `return_url_data=True`, else `None` |
| `product_artifact` | `ProductDataArtifact` | Contains `product_file_path`, `scraped_count`, `failed_count` |
| `product_data` | `dict | None` | Product data if `return_prod_data=True`, else `None` |


---


## 📁 Output Structure


All artifacts are saved under timestamped directories:


```text
Artifacts/
└── 12_04_2025_14_58_45/           # Timestamp: MM_DD_YYYY_HH_MM_SS
    ├── UrlData/
    │   └── urls.json              # Collected product URLs
    └── ProductData/
        └── products.json          # Detailed product data
```


### URL JSON Format


```json
{
  "total_products": 2,
  "total_urls": 3,
  "products": {
    "laptop": {
      "count": 1,
      "urls": ["https://www.amazon.in/..."]
    },
    "wireless mouse": {
      "count": 2,
      "urls": [
        "https://www.amazon.in/...",
        "https://www.amazon.in/..."
      ]
    }
  }
}
```


### Product JSON Format


```json
{
  "total_scraped": 3,
  "total_failed": 0,
  "products": {
    "laptop": [
      {
        "Product Name": "Apple MacBook Air M2",
        "Product Price": "₹99,999",
        "Ratings": "4.5",
        "Total Reviews": "1,234 ratings",
        "Category": "Computers & Accessories",
        "Product URL": "https://www.amazon.in/...",
        "Technical Details": {
          "Brand": "Apple",
          "Processor": "M2",
          "RAM": "8GB"
        },
        "Customer Reviews": [
          {
            "reviewer": "John Doe",
            "rating": "5.0",
            "title": "Excellent laptop",
            "content": "Fast and reliable..."
          }
        ]
      }
    ]
  }
}
```


---


## 🔧 Advanced Examples


### Example: Different Link Counts per Search Term


```python
pipeline = AmazonScrapingPipeline(
    search_terms=['laptop', 'wireless mouse', 'keyboard'],
    target_links=[10, 5, 3],  # 10 laptops, 5 mice, 3 keyboards
    headless=True,
    return_url_data=True,
    return_prod_data=True
)


url_artifact, url_data, product_artifact, product_data = pipeline.run_pipeline()
```


### Example: URL Scraping Only


```python
from scrapper.pipeline.url_pipeline import AmazonUrlScrapingPipeline


pipeline = AmazonUrlScrapingPipeline(
    search_terms=['gaming laptop'],
    target_links=20,
    headless=True,
    return_url_data=True
)


url_artifact, url_data = pipeline.run()


# Review URLs before product scraping
for term, data in url_data['products'].items():
    print(f"{term}: {data['count']} URLs")
```


### Example: Product Scraping from Existing URLs


```python
from scrapper.pipeline.prodcut_pipeline import AmazonProductScrapingPipeline


pipeline = AmazonProductScrapingPipeline(
    url_file_path="Artifacts/12_04_2025_14_58_45/UrlData/urls.json",
    headless=True,
    return_prod_data=True
)


product_artifact, product_data = pipeline.run()


print(f"Success: {product_artifact.scraped_count}")
print(f"Failed: {product_artifact.failed_count}")
```


---


## 🌐 Using the REST API


### Example: Python Requests


```python
import requests


# Main scraper
response = requests.post(
    'http://127.0.0.1:8080/api/mainscrape',
    json={
        'search_terms': ['laptop'],
        'target_links': 5,
        'headless': True,
        'return_url_data': True,
        'return_prod_data': True
    }
)


data = response.json()
print(f"Status: {data['status']}")
print(f"URLs: {data['url_data']['total_urls']}")
print(f"Products: {data['product_data']['total_scraped']}")


# Download files
timestamp = "12_04_2025_14_58_45"
url_file = requests.get(f'http://127.0.0.1:8080/api/download/url-data/{timestamp}')
with open('urls.json', 'wb') as f:
    f.write(url_file.content)
```


### Example: JavaScript/Node.js


```javascript
// Main scraper
const response = await fetch('http://127.0.0.1:8080/api/mainscrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    search_terms: ['laptop'],
    target_links: 5,
    headless: true,
    return_url_data: true,
    return_prod_data: true
  })
});


const data = await response.json();
console.log(`URLs: ${data.url_data.total_urls}`);
console.log(`Products: ${data.product_data.total_scraped}`);
```


---


## 🛠️ Project Layout


```text
project/
├── Artifacts/
│   └── <timestamp_folder>/
│       ├── UrlData/
│       │   └── urls.json
│       └── ProductData/
│           └── products.json
├── logs/
│   ├── *.log
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   ├── index.html
│   ├── base.html
│   └── about.html
└── scrapper/
    ├── config/
    │   ├── urls_locators.yaml
    │   └── product_locators.yaml
    ├── constant/
    │   └── configuration.py
    ├── entity/
    │   ├── artifact_entity.py
    │   ├── config_entity.py
    │   ├── product_locator_entity.py
    │   └── url_locator_entity.py
    ├── exception/
    │   └── custom_exception.py
    ├── logger/
    │   └── logging.py
    ├── pipeline/
    │   ├── main_pipeline.py
    │   ├── url_pipeline.py
    │   └── prodcut_pipeline.py
    ├── router/
    │   └── api.py              # FastAPI application
    ├── src/
    │   ├── multi_product_scrapper.py
    │   ├── multi_url_scrapper.py
    │   └── url_scrapper.py
    └── util/
        └── main_utils.py
```


---


## 📊 Logging


Logs are stored in the `logs/` directory with timestamps:


```text
logs/
├── 12_04_2025_14_58_45.log
├── 12_04_2025_15_30_12.log
└── ...
```


**Log Levels:**
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Errors during scraping
- DEBUG: Detailed debugging information


---


## 🚨 Important Notes


### Legal & Ethical Considerations


- ⚠️ **Educational purposes only** - Use responsibly
- ⚠️ Respect Amazon's Terms of Service and robots.txt
- ⚠️ Use reasonable delays between requests
- ⚠️ Do not overload Amazon's servers
- ⚠️ Check local laws regarding web scraping
- ⚠️ This tool should not be used for commercial scraping without proper authorization


### Technical Considerations


- Amazon's DOM structure may change; locators may need updates
- Anti-bot mechanisms may block excessive requests
- Headless mode is recommended for production use
- Use proxies for large-scale scraping
- The FastAPI server runs on port 8080 by default (configurable)
- For production deployment, use a proper ASGI server like Gunicorn with Uvicorn workers


---


## 🔄 Typical Workflows


### Option 1: Use Web UI


1. Start the server: `uvicorn scrapper.router.api:app --host 127.0.0.1 --port 8080`
2. Open [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
3. Select a scraper tab
4. Configure options and click "Start Scraping"
5. Download results when complete


### Option 2: Use REST API


```bash
# Full pipeline
curl -X POST "http://127.0.0.1:8080/api/mainscrape" \
  -H "Content-Type: application/json" \
  -d '{
    "search_terms": ["laptop"],
    "target_links": 5,
    "headless": true,
    "return_url_data": true,
    "return_prod_data": true
  }'


# Download results
curl -O "http://127.0.0.1:8080/api/download/url-data/12_04_2025_14_58_45"
```


### Option 3: Use Python Directly


```python
from scrapper.pipeline.main_pipeline import AmazonScrapingPipeline


pipeline = AmazonScrapingPipeline(
    search_terms=['laptop pc', 'wireless mouse'],
    target_links=[1, 2],
    headless=True,
    return_url_data=True,
    return_prod_data=True
)


url_artifact, url_data, product_artifact, product_data = pipeline.run_pipeline()
```


### Option 4: Run Stages Independently


```bash
# 1) Collect URLs
python -m scrapper.pipeline.url_pipeline


# 2) Scrape products (update url_file_path first)
python -m scrapper.pipeline.prodcut_pipeline
```


---


## 📄 License


**Proprietary License** - All rights reserved.


This software is proprietary. No part of this code may be used, copied, modified, or distributed without explicit written permission from the copyright holder.


---


## 👨‍💻 Support


For support, bug reports, or feature requests:
- 📧 Email: [support.dhruv@dhruvsaxena25.com](mailto:support.dhruv@dhruvsaxena25.com)
- 🐛 Issues: Create an issue on the repository
- 📖 Documentation: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) (when server is running)


---


## 🔄 Version History


### 1.0.0 (Current)
- ✅ Initial release
- ✅ URL scraping pipeline
- ✅ Product scraping pipeline
- ✅ End-to-end pipeline
- ✅ FastAPI REST API
- ✅ Web UI interface
- ✅ Download endpoints
- ✅ Comprehensive logging
- ✅ YAML-based locators


---


## 🎓 More Information


For interactive API documentation with live testing capabilities, visit:
- **Swagger UI**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- **ReDoc**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)


(Available when the FastAPI server is running)


---


**Made with ❤️ for Amazon scraping workflows by Dhruv Saxena**

**Also Visit: [dhruvsaxena25.com](https://dhruvsaxena25.com/) for more details.**


---


> **Disclaimer**: This project is proprietary. No one is allowed to use, copy, modify, or distribute any part of this code without explicit permission from the owner.
