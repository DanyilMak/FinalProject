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
