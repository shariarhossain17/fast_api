import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate, UserOut, UserUpdate

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI_WITH_POSTGRES"),
    description="A CRUD API for user management with PostgreSQL",
    version="1.0.0"
)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test route
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


#create add a new user

@app.post("/user",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def create_user(payload:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(
        (User.email==payload.email) | User.username==payload.username
    ).first()

    print(existing_user)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already exist"
        )
    
    #create user
    user = User(email=payload.email,username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

