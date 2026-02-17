from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .database import engine, Base, get_db
from . import crud, schemas
from .models import User
from .auth import create_access_token, verify_password
from .routers import users, products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Shop API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.email, user.name, user.password)


@app.post("/auth/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}