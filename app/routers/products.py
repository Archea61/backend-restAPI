from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..models import Product
from ..auth import get_admin_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return crud.create_product(db, product.name, product.price)


@router.get("/", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()