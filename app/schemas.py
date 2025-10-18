from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class ProductBase(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass  # same fields when creating

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float
    product: ProductOut

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total_price: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    quantity: Union[int, None] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True