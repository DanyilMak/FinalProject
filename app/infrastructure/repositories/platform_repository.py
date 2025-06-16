from sqlalchemy.orm import Session
from app.domain.models.schemas import PlatformCreate
from app.domain.entities.models import Platform

class PlatformRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Platform).all()

    def get(self, platform_id: int):
        return self.db.query(Platform).filter(Platform.id == platform_id).first()

    def create(self, platform: PlatformCreate):
        db_platform = Platform(**platform.dict())
        self.db.add(db_platform)
        self.db.commit()
        self.db.refresh(db_platform)
        return db_platform

    def delete(self, platform_id: int):
        platform = self.get(platform_id)
        if platform:
            self.db.delete(platform)
            self.db.commit()
        return platform
