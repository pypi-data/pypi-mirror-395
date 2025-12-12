"""
Amazon Scraper Router API with Integrated Frontend and Download Features
"""

from datetime import datetime
from pathlib import Path
from typing import List, Union
import json

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from scrapper.pipeline.main_pipeline import AmazonScrapingPipeline
from scrapper.pipeline.prodcut_pipeline import AmazonProductScrapingPipeline
from scrapper.pipeline.url_pipeline import AmazonUrlScrapingPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Amazon Scraper Router",
    version="1.0.0",
    description="A FastAPI router for Amazon scraping pipeline operations"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== Request Models ====================

class ScrapeRequest(BaseModel):
    """Request model for main scraping pipeline."""
    search_terms: List[str] = Field(
        ...,
        description="List of search terms to scrape"
    )
    target_links: Union[int, List[int]] = Field(
        ...,
        description="Number of target links to scrape per search term"
    )
    headless: bool = Field(
        True,
        description="Run browser in headless mode"
    )
    return_url_data: bool = Field(
        False,
        description="Return URL data in memory"
    )
    return_prod_data: bool = Field(
        False,
        description="Return product data in memory"
    )

class URLScrapeRequest(BaseModel):
    """Request model for URL scraping pipeline."""
    search_terms: List[str] = Field(
        ...,
        description="List of search terms to scrape"
    )
    target_links: Union[int, List[int]] = Field(
        ...,
        description="Number of target links to scrape per search term"
    )
    headless: bool = Field(
        True,
        description="Run browser in headless mode"
    )
    return_url_data: bool = Field(
        False,
        description="Return URL data in memory"
    )

class ProductScrapeRequest(BaseModel):
    """Request model for product scraping pipeline."""
    headless: bool = Field(
        True,
        description="Run browser in headless mode"
    )
    return_prod_data: bool = Field(
        False,
        description="Return product data in memory"
    )

    @classmethod
    def as_form(
        cls,
        headless: bool = Form(True),
        return_prod_data: bool = Form(False)
    ):
        """Convert form data to Pydantic model."""
        return cls(headless=headless, return_prod_data=return_prod_data)

# ==================== Frontend Endpoints ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main frontend interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page with application information."""
    return templates.TemplateResponse("about.html", {"request": request})

# ==================== API Endpoints ====================

@app.get("/api")
def api_root():
    """API root endpoint - health check."""
    return {"message": "Amazon Scraper Router API is running.", "version": "1.0.0"}

@app.post("/api/mainscrape")
def main_scrape(request: ScrapeRequest):
    """Execute main scraping pipeline."""
    pipeline = AmazonScrapingPipeline(
        search_terms=request.search_terms,
        target_links=request.target_links,
        headless=request.headless,
        return_url_data=request.return_url_data,
        return_prod_data=request.return_prod_data
    )

    result = pipeline.run_pipeline()

    # Unpack result based on return flags
    if request.return_url_data and request.return_prod_data:
        url_artifact, url_data, product_artifact, product_data = result
    elif request.return_url_data and not request.return_prod_data:
        url_artifact, url_data, product_artifact = result
        product_data = None
    elif not request.return_url_data and request.return_prod_data:
        url_artifact, product_artifact, product_data = result
        url_data = None
    else:
        url_artifact, product_artifact = result
        url_data = None
        product_data = None

    # Build response
    response = {
        "status": "success",
        "url_artifact": {
            "url_file_path": url_artifact.url_file_path,
            "download_url": f"/api/download/file?path={url_artifact.url_file_path}"
        },
        "product_artifact": {
            "product_file_path": product_artifact.product_file_path,
            "download_url": f"/api/download/file?path={product_artifact.product_file_path}"
        },
    }

    if request.return_url_data:
        response["url_data"] = url_data

    if request.return_prod_data:
        response["product_data"] = product_data

    return response

@app.post("/api/urlscrape")
def url_scrape(request: URLScrapeRequest):
    """Execute URL scraping pipeline."""
    pipeline = AmazonUrlScrapingPipeline(
        search_terms=request.search_terms,
        target_links=request.target_links,
        headless=request.headless,
        return_url_data=request.return_url_data
    )

    result = pipeline.run()

    # Unpack result based on return flag
    if request.return_url_data:
        url_artifact, url_data = result
    else:
        (url_artifact,) = result
        url_data = None

    response = {
        "status": "success",
        "url_artifact": {
            "url_file_path": url_artifact.url_file_path,
            "download_url": f"/api/download/file?path={url_artifact.url_file_path}"
        }
    }

    if request.return_url_data:
        response["url_data"] = url_data

    return response

@app.post("/api/productscrape")
async def product_scrape(
    file: UploadFile = File(..., description="JSON file containing product URLs"),
    request: ProductScrapeRequest = Depends(ProductScrapeRequest.as_form)
):
    """Execute product scraping pipeline."""
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    url_data_dir = Path(f"Artifacts/{timestamp}/UrlData")
    url_data_dir.mkdir(parents=True, exist_ok=True)
    url_file_path = url_data_dir / "urls.json"

    try:
        content = await file.read()
        json_data = json.loads(content)

        with open(url_file_path, 'wb') as f:
            f.write(content)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )
    finally:
        await file.close()

    pipeline = AmazonProductScrapingPipeline(
        url_file_path=str(url_file_path),
        headless=request.headless,
        return_prod_data=request.return_prod_data
    )

    result = pipeline.run()

    if request.return_prod_data:
        product_artifact, product_data = result
    else:
        (product_artifact,) = result
        product_data = None

    response = {
        "status": "success",
        "url_file_path": str(url_file_path),
        "url_artifact": {
            "url_file_path": str(url_file_path),
            "download_url": f"/api/download/file?path={url_file_path}"
        },
        "product_artifact": {
            "product_file_path": product_artifact.product_file_path,
            "download_url": f"/api/download/file?path={product_artifact.product_file_path}"
        }
    }

    if request.return_prod_data:
        response["product_data"] = product_data

    return response

# ==================== Download Endpoints ====================

@app.get("/api/download/file")
async def download_file(path: str):
    """
    Download a file by its path.
    
    Args:
        path: File path relative to project root
    """
    file_path = Path(path)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Path is not a file")
    
    # Ensure the file is within the Artifacts directory for security
    try:
        file_path.resolve().relative_to(Path.cwd() / "Artifacts")
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type='application/json'
    )

@app.get("/api/download/url-data/{timestamp}")
async def download_url_data(timestamp: str):
    """
    Download URL data JSON file by timestamp.
    
    Args:
        timestamp: Timestamp in format MM_DD_YYYY_HH_MM_SS
    """
    file_path = Path(f"Artifacts/{timestamp}/UrlData/urls.json")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="URL data file not found")
    
    return FileResponse(
        path=file_path,
        filename=f"urls_{timestamp}.json",
        media_type='application/json'
    )

@app.get("/api/download/product-data/{timestamp}")
async def download_product_data(timestamp: str):
    """
    Download product data JSON file by timestamp.
    
    Args:
        timestamp: Timestamp in format MM_DD_YYYY_HH_MM_SS
    """
    file_path = Path(f"Artifacts/{timestamp}/ProductData/products.json")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Product data file not found")
    
    return FileResponse(
        path=file_path,
        filename=f"products_{timestamp}.json",
        media_type='application/json'
    )


@app.get("/api/results/{timestamp}")
def get_results(timestamp: str):
    """Retrieve scraping results by timestamp."""
    try:
        url_file = Path(f"Artifacts/{timestamp}/UrlData/urls.json")
        product_file = Path(f"Artifacts/{timestamp}/ProductData/products.json")
        
        response = {
            "timestamp": timestamp,
            "download_urls": {}
        }
        
        if url_file.exists():
            with open(url_file, 'r') as f:
                url_data = json.load(f)
                response["url_data"] = url_data
                response["download_urls"]["url_data"] = f"/api/download/url-data/{timestamp}"
        
        if product_file.exists():
            with open(product_file, 'r') as f:
                product_data = json.load(f)
                response["product_data"] = product_data
                response["download_urls"]["product_data"] = f"/api/download/product-data/{timestamp}"
        
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Results not found: {str(e)}")

@app.get("/api/results")
def list_results():
    """List all available scraping results."""
    artifacts_dir = Path("Artifacts")
    if not artifacts_dir.exists():
        return {"results": []}
    
    results = []
    for timestamp_dir in sorted(artifacts_dir.iterdir(), reverse=True):
        if timestamp_dir.is_dir():
            timestamp = timestamp_dir.name
            result_entry = {
                "timestamp": timestamp,
                "files": {},
                "download_urls": {}
            }
            
            url_file = timestamp_dir / "UrlData" / "urls.json"
            product_file = timestamp_dir / "ProductData" / "products.json"
            
            if url_file.exists():
                result_entry["files"]["url_file"] = str(url_file)
                result_entry["download_urls"]["url_data"] = f"/api/download/url-data/{timestamp}"
            
            if product_file.exists():
                result_entry["files"]["product_file"] = str(product_file)
                result_entry["download_urls"]["product_data"] = f"/api/download/product-data/{timestamp}"
            
            results.append(result_entry)
    
    return {"results": results}

# ==================== Application Entry Point ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
