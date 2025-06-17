from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.entities.models import Product, Platform, ScrapedProductData
from app.infrastructure.db.db import SessionLocal
from app.services.scraper import scrape_platform
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{product_id}")
def scrape_all(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    platforms = db.query(Platform).all()
    if not platforms:
        raise HTTPException(status_code=400, detail="No platforms configured")

    scraped_results = []
    for platform in platforms:
        result = scrape_platform(platform, product.global_query_name)
        if result:
            scraped = ScrapedProductData(
                product_id=product.id,
                platform_id=platform.id,
                scraped_at=datetime.utcnow(),
                **result
            )
            db.add(scraped)
            scraped_results.append(scraped)

    db.commit()
    return {"scraped": len(scraped_results)}

@router.post("/{product_id}/platform/{platform_id}")
def scrape_single_platform(product_id: int, platform_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")

    result = scrape_platform(platform, product.global_query_name)
    if not result:
        raise HTTPException(status_code=500, detail=f"Failed to scrape from platform {platform.name}")

    scraped = ScrapedProductData(
        product_id=product.id,
        platform_id=platform.id,
        scraped_at=datetime.utcnow(),
        **result
    )
    db.add(scraped)
    db.commit()
    db.refresh(scraped)

    return {
        "scraped_id": scraped.id,
        "platform": platform.name,
        "product": product.global_query_name,
        "price": scraped.price,
        "url_on_platform": scraped.url_on_platform
    }
