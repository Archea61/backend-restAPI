from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..auth import get_current_user
from ..models import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_order(db, current_user.id, order.items)


@router.get("/my", response_model=list[schemas.OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()