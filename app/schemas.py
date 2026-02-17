from pydantic import BaseModel, EmailStr
from typing import List




class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        from_attributes = True




class ProductCreate(BaseModel):
    name: str
    price: float


class ProductOut(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True




class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    total_price: float
    items: List[OrderItemOut]

    class Config:
        from_attributes = True




class Token(BaseModel):
    access_token: str
    token_type: str