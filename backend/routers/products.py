from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from backend.db_connect import SessionLocal
from backend.models import Product
from backend.models.product import ProductCreate

# Tworzenie instancji routera
product_router = APIRouter()

# Zależność do uzyskania sesji bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.get("/product_list")
def get_product_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(8, ge=1),
    gender: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):
    print(f"Received filters: gender={gender}, sort={sort}")
    query = db.query(Product)

    # Filtrowanie według płci
    if gender:
        query = query.filter(Product.gender == gender)

    # Sortowanie
    if sort == "new_price":
        query = query.order_by(asc(Product.new_price))
    elif sort == "-new_price":
        query = query.order_by(desc(Product.new_price))

    # Liczba wszystkich wyników
    total_items = query.count()

    # Paginacja
    query = query.offset((page - 1) * per_page).limit(per_page)
    products = query.all()

    # Obliczanie liczby stron
    total_pages = (total_items + per_page - 1) // per_page

    return {
        "data": products,
        "first": 1,
        "prev": page - 1 if page > 1 else None,
        "next": page + 1 if page < total_pages else None,
        "last": total_pages,
        "pages": total_pages,
        "items": total_items,
    }

@product_router.post("/products")
def product_add(product: ProductCreate, db: Session = Depends(get_db)):
    # Tworzymy produkt w bazie danych
    new_product = Product(
        name=product.name,
        category=product.category,
        gender=product.gender,
        new_price=product.new_price,
        old_price=product.old_price,
        amount=product.amount,
        description=product.description,
        picture=product.picture,
    )

    # Dodanie produktu do sesji i zapisanie do bazy danych
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@product_router.get("/products")
def get_product_list(db: Session = Depends(get_db)):
    products = db.query(Product).all()  # Query all products from the database
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return {"data": products}