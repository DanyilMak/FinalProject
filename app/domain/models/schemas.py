from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PlatformCreate(BaseModel):
    name: str
    base_url: str
    search_url_template: str

class PlatformRead(PlatformCreate):
    id: int

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    global_query_name: str
    description: Optional[str]

class ProductRead(ProductCreate):
    id: int

    class Config:
        orm_mode = True


class ScrapedProductDataRead(BaseModel):
    id: int
    product_id: int
    platform_id: int
    url_on_platform: Optional[str]
    name_on_platform: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    rating: Optional[float]
    reviews_count: Optional[int]
    availability_status: Optional[str]
    scraped_at: datetime
    search_position: Optional[int]

    class Config:
        orm_mode = True


class RegressionModelRead(BaseModel):
    id: int
    name: str
    platform_id: Optional[int]
    target_variable: str
    feature_variables: List[str]
    coefficients_json: dict
    intercept: float
    r_squared: float
    last_trained_at: datetime

    class Config:
        orm_mode = True
