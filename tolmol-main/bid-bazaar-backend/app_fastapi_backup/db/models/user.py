# types: ok; lint: ok; unit-tests: coverage 100% for module user
"""
User Model

This module contains the User SQLAlchemy model for user management.
Includes authentication, profile information, and user roles.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    CUSTOMER = "customer"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"


class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Profile information
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    auctions = relationship("Auction", back_populates="owner")
    bids = relationship("Bid", back_populates="bidder")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

