from sqlalchemy.orm import Session
from app.domain.entities.models import RegressionModel
from typing import List
from datetime import datetime

class RegressionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_model(self, name: str, platform_id: int, target: str, features: List[str],
                   coefficients: dict, intercept: float, r_squared: float):
        model = RegressionModel(
            name=name,
            platform_id=platform_id,
            target_variable=target,
            feature_variables=features,
            coefficients_json=coefficients,
            intercept=intercept,
            r_squared=r_squared,
            last_trained_at=datetime.utcnow()
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_all(self):
        return self.db.query(RegressionModel).all()

    def get_by_id(self, model_id: int):
        return self.db.query(RegressionModel).filter(RegressionModel.id == model_id).first()

    def get_latest_by_platform(self, platform_id: int):
        return (
            self.db.query(RegressionModel)
            .filter(RegressionModel.platform_id == platform_id)
            .order_by(RegressionModel.last_trained_at.desc())
            .first()
        )
