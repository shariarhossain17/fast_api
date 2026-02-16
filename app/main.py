import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import or_
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

@app.post("/user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(
            User.email == payload.email,
            User.username == payload.username
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already exist"
        )
    
    user = User(email=payload.email, username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.put("/user/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    # Get existing user
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Update email if provided and different
    if payload.email and payload.email != user.email:
        # Check if email already taken
        if db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        user.email = payload.email

    # Update username if provided and different
    if payload.username and payload.username != user.username:
        # Check if username already taken
        if db.query(User).filter(User.username == payload.username).first():
            raise HTTPException(
                status_code=400,
                detail="Username already in use"
            )
        user.username = payload.username

    db.add(user)        # Mark as modified
    db.commit()         # Save changes
    db.refresh(user)    # Reload from database

    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)     # Mark for deletion
    db.commit()         # Execute deletion

    return None         # 204 responses have no body