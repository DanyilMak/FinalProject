from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    search_url_template = Column(String, nullable=False)

    scraped_data = relationship("ScrapedProductData", back_populates="platform")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    global_query_name = Column(String, nullable=False)
    description = Column(String)

    scraped_data = relationship("ScrapedProductData", back_populates="product")

class ScrapedProductData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))

    url_on_platform = Column(String)
    name_on_platform = Column(String)
    price = Column(Float)
    currency = Column(String)
    rating = Column(Float)
    reviews_count = Column(Integer)
    availability_status = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    search_position = Column(Integer, nullable=True)

    product = relationship("Product", back_populates="scraped_data")
    platform = relationship("Platform", back_populates="scraped_data")

class RegressionModel(Base):
    __tablename__ = "regression_models"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    target_variable = Column(String)
    feature_variables = Column(JSON)
    coefficients_json = Column(JSON)
    intercept = Column(Float)
    r_squared = Column(Float)
    last_trained_at = Column(DateTime)
