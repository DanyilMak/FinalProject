import statsmodels.api as sm
from sqlalchemy.orm import Session
from app.domain.entities.models import ScrapedProductData
from typing import List, Dict
import pandas as pd

def train_model(db: Session, platform_id: int, target: str = "search_position", features: List[str] = ["price"]):
    query = db.query(ScrapedProductData).filter(ScrapedProductData.platform_id == platform_id)
    rows = query.all()

    if not rows:
        return None

    # Вибираємо тільки ті записи, де є всі необхідні поля
    data = []
    for row in rows:
        record = {}
        missing = False
        for f in features + [target]:
            value = getattr(row, f)
            if value is None:
                missing = True
                break
            record[f] = value
        if not missing:
            data.append(record)

    if len(data) < 3:
        return None

    df = pd.DataFrame(data)
    X = sm.add_constant(df[features])
    y = df[target]

    model = sm.OLS(y, X).fit()

    return {
        "coefficients": dict(model.params.drop("const")),
        "intercept": model.params["const"],
        "r_squared": model.rsquared
    }
