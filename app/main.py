from fastapi import FastAPI
from app.api.routes import platforms, products, scraped_data, scraping

app = FastAPI(
    title="Final Project - Price Analyzer",
    version="0.1.0"
)

app.include_router(platforms.router, prefix="/platforms", tags=["Platforms"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(scraped_data.router, prefix="/scraped", tags=["Scraped Data"])
app.include_router(scraping.router, prefix="/scrape", tags=["Scraping"])