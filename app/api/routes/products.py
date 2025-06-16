from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.models.schemas import ProductCreate, ProductRead
from typing import List

from app.infrastructure.db.db import SessionLocal
from app.infrastructure.repositories.product_repository import ProductRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.create(product)

@router.get("/", response_model=List[ProductRead])
def read_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_all()

@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    result = repo.delete(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
