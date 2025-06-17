from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.db import SessionLocal
from app.infrastructure.repositories.regression_repository import RegressionRepository
from app.services.regression import train_model
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/train/")
def train(platform_id: int, db: Session = Depends(get_db)):
    features = ["price", "reviews_count", "rating"]
    result = train_model(db, platform_id, target="search_position", features=features)
    if not result:
        raise HTTPException(status_code=400, detail="Недостатньо даних для навчання моделі")

    repo = RegressionRepository(db)
    model = repo.save_model(
        name=f"Regression for platform {platform_id}",
        platform_id=platform_id,
        target="search_position",
        features=features,
        coefficients=result["coefficients"],
        intercept=result["intercept"],
        r_squared=result["r_squared"]
    )
    return {
        "id": model.id,
        "r_squared": model.r_squared,
        "coefficients": model.coefficients_json,
        "intercept": model.intercept
    }

@router.get("/")
def get_models(db: Session = Depends(get_db)):
    repo = RegressionRepository(db)
    return repo.get_all()

class PredictRequest(BaseModel):
    price: float
    rating: float
    reviews_count: int
    model_id: Optional[int] = None
    platform_id: Optional[int] = None

@router.post("/predict/")
def predict(request: PredictRequest, db: Session = Depends(get_db)):
    repo = RegressionRepository(db)

    if request.model_id:
        model = repo.get_by_id(request.model_id)
    elif request.platform_id:
        model = repo.get_latest_by_platform(request.platform_id)
    else:
        raise HTTPException(status_code=400, detail="Необхідно передати model_id або platform_id")

    if not model:
        raise HTTPException(status_code=404, detail="Модель не знайдена")

    features = model.feature_variables
    values = [getattr(request, f) for f in features]

    # y = b0 + b1*x1 + b2*x2 + ...
    prediction = model.intercept
    for i, f in enumerate(features):
        prediction += model.coefficients_json.get(f, 0) * values[i]

    return {
        "prediction": prediction,
        "model_id": model.id,
        "platform_id": model.platform_id,
        "used_features": {f: values[i] for i, f in enumerate(features)}
    }