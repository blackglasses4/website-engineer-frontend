import enum
from unicodedata import category
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image , image_attachment
from typing import Optional
from pydantic import BaseModel
from backend.base import Base

class GenderEnum(enum.Enum):
    man = "Mężczyźni"
    woman = "Kobiety"
    unisex = "Dla obu płci"
    
class CategoryEnum(enum.Enum):
    shirt = "koszulka"
    jacket = "kurtka"
    pants = "spodnie"
    hat = "czapka"
    outfit = "stroje"

class Product(Base):
    __tablename__ = 'products' #Nazwa tabeli w bazie danych
    
    id = Column(Integer, primary_key=True, index=True)      #
    name = Column(String(255), nullable=False) 
    category = Column(Enum(CategoryEnum), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    new_price = Column(Integer, nullable=False)
    old_price = Column(Integer, nullable=True)        # Nazwy kolumn w bazie
    amount = Column(Integer, nullable=True)     #
    description = Column(String(255), nullable=True) 
    picture = image_attachment('ProductPicture')
    
    # Establish bidirectional relationship
    pictures = relationship('ProductPicture', back_populates='product')

class ProductCreate(BaseModel):
    name: str
    category: CategoryEnum
    gender: GenderEnum
    new_price: int
    old_price: Optional[int] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    picture: Optional[str] = None  # Path or URL to the image

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models