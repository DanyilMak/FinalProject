from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.models.schemas import ScrapedProductDataRead
from typing import List

from app.infrastructure.db.db import SessionLocal
from app.infrastructure.repositories.scraped_data_repository import ScrapedDataRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ScrapedProductDataRead])
def get_all_scraped(db: Session = Depends(get_db)):
    repo = ScrapedDataRepository(db)
    return repo.get_all()

@router.get("/product/{product_id}", response_model=List[ScrapedProductDataRead])
def get_by_product(product_id: int, db: Session = Depends(get_db)):
    repo = ScrapedDataRepository(db)
    return repo.get_by_product(product_id)

@router.delete("/{scraped_id}", response_model=ScrapedProductDataRead)
def delete_scraped(scraped_id: int, db: Session = Depends(get_db)):
    repo = ScrapedDataRepository(db)
    result = repo.delete(scraped_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return result
