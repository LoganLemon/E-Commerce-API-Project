import os
import stripe
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Gather cart items
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2. Build Stripe line items
    line_items = []
    total = 0
    for item in cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()
        if not product or product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} not available or out of stock",
            )

        # Stripe requires amounts in cents
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": int(product.price * 100),
            },
            "quantity": item.quantity,
        })
        total += product.price * item.quantity

    # 3. Create Stripe Checkout Session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://127.0.0.1:8000/orders/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/orders/cancel",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 4. Return the session URL for front-end redirect
    return JSONResponse({"checkout_url": session.url})

@router.get("/success")
def payment_success(session_id: str, db: Session = Depends(get_db)):
    session = stripe.checkout.Session.retrieve(session_id)
    customer_email = session.customer_details.email if session.customer_details else None
    return {"message": "Payment successful", "email": customer_email}

@router.get("/cancel")
def payment_cancel():
    return {"message": "Payment canceled or failed"}