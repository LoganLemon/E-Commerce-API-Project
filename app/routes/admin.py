from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

# ------------------ CREATE PRODUCT ------------------ #
@router.post("/products", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ------------------ UPDATE PRODUCT ------------------ #
@router.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    updated_data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_data.name or product.name
    product.description = updated_data.description or product.description
    product.price = updated_data.price or product.price
    product.quantity = updated_data.quantity or product.quantity

    db.commit()
    db.refresh(product)
    return product


# ------------------ DELETE PRODUCT ------------------ #
@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}


# ------------------ GET ALL PRODUCTS ------------------ #
@router.get("/products", response_model=list[schemas.ProductOut])
def get_all_products(
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    products = db.query(models.Product).all()
    return products
