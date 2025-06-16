from sqlalchemy.orm import Session
from app.domain.entities.models import ScrapedProductData
from app.domain.models.schemas import ScrapedProductDataRead
from typing import List, Optional
from datetime import datetime

class ScrapedDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ScrapedProductData]:
        return self.db.query(ScrapedProductData).all()

    def get_by_product(self, product_id: int) -> List[ScrapedProductData]:
        return self.db.query(ScrapedProductData).filter(ScrapedProductData.product_id == product_id).all()

    def delete(self, scraped_id: int) -> Optional[ScrapedProductData]:
        obj = self.db.query(ScrapedProductData).filter(ScrapedProductData.id == scraped_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
