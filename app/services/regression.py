import statsmodels.api as sm
from sqlalchemy.orm import Session
from app.domain.entities.models import ScrapedProductData
from typing import List, Dict

def train_model(db: Session, platform_id: int, target: str = "search_position", features: List[str] = ["price", "reviews_count", "rating"]):
    query = db.query(ScrapedProductData).filter(ScrapedProductData.platform_id == platform_id)
    rows = query.all()

    if not rows:
        return None

    data = [{f: getattr(row, f) for f in features + [target]} for row in rows if all(getattr(row, f) is not None for f in features + [target])]

    if len(data) < 3:
        return None

    import pandas as pd
    df = pd.DataFrame(data)

    X = sm.add_constant(df[features])
    y = df[target]

    model = sm.OLS(y, X).fit()

    return {
        "coefficients": dict(model.params.drop("const")),
        "intercept": model.params["const"],
        "r_squared": model.rsquared
    }
