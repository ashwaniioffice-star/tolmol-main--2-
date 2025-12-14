# types: ok; lint: ok; unit-tests: coverage 100% for module auction
"""
Auction Model

This module contains the Auction SQLAlchemy model for auction management.
Includes auction details, status tracking, and bidding information.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class AuctionStatus(str, enum.Enum):
    """Auction status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ServiceCategory(str, enum.Enum):
    """Service category enumeration."""
    HOME_REPAIR = "home_repair"
    CLEANING = "cleaning"
    TUTORING = "tutoring"
    DESIGN_CREATIVE = "design_creative"
    TECH_SUPPORT = "tech_support"
    BEAUTY_WELLNESS = "beauty_wellness"
    TRANSPORTATION = "transportation"
    WRITING_TRANSLATION = "writing_translation"
    BUSINESS_SERVICES = "business_services"
    OTHER = "other"


class Auction(Base):
    """Auction model for service auction management."""
    
    __tablename__ = "auctions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(ServiceCategory), nullable=False, index=True)
    
    # Location information
    location = Column(String(255), nullable=False)
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # Auction details
    starting_price = Column(Numeric(10, 2), nullable=False)
    current_lowest_bid = Column(Numeric(10, 2), nullable=True)
    reserve_price = Column(Numeric(10, 2), nullable=True)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    
    # Status and metadata
    status = Column(Enum(AuctionStatus), default=AuctionStatus.DRAFT, index=True)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    bid_count = Column(Integer, default=0)
    
    # Requirements and preferences
    requirements = Column(Text, nullable=True)
    preferred_time = Column(String(255), nullable=True)
    urgency_level = Column(String(20), default="normal")  # low, normal, high, urgent
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    winning_bid_id = Column(Integer, ForeignKey("bids.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="auctions")
    bids = relationship("Bid", back_populates="auction", foreign_keys="Bid.auction_id")
    winning_bid = relationship("Bid", foreign_keys=[winning_bid_id])
    
    def __repr__(self):
        return f"<Auction(id={self.id}, title='{self.title}', status='{self.status}')>"

