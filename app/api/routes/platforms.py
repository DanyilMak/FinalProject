from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.models.schemas import PlatformCreate, PlatformRead
from app.infrastructure.db.db import SessionLocal
from app.infrastructure.repositories.platform_repository import PlatformRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlatformRead)
def create_platform(platform: PlatformCreate, db: Session = Depends(get_db)):
    repo = PlatformRepository(db)
    return repo.create(platform)

@router.get("/", response_model=List[PlatformRead])
def read_platforms(db: Session = Depends(get_db)):
    repo = PlatformRepository(db)
    return repo.get_all()

@router.delete("/{platform_id}", response_model=PlatformRead)
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    repo = PlatformRepository(db)
    result = repo.delete(platform_id)
    if not result:
        raise HTTPException(status_code=404, detail="Platform not found")
    return result
