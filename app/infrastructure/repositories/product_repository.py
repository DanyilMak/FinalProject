from sqlalchemy.orm import Session
from app.domain.models.schemas import ProductCreate
from app.domain.entities.models import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Product).all()

    def get(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product: ProductCreate):
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, product_id: int):
        product = self.get(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
        return product
