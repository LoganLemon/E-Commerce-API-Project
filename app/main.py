import os
from dotenv import load_dotenv
import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import users, products, carts, orders, admin

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(orders.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "API is running"}

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)