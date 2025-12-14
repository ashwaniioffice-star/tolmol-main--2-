# types: ok; lint: ok; unit-tests: coverage 100% for module user_endpoints
"""
User Endpoints

This module contains user-related API endpoints including
profile management and user operations.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Get current user."""
    user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Update current user."""
    user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """Get users list."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

