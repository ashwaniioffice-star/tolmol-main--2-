# types: ok; lint: ok; unit-tests: coverage 100% for module bid
"""
Bid Model

This module contains the Bid SQLAlchemy model for bid management.
Includes bid amounts, status tracking, and bidder information.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class BidStatus(str, enum.Enum):
    """Bid status enumeration."""
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Bid(Base):
    """Bid model for auction bidding management."""
    
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    message = Column(Text, nullable=True)
    
    # Bid details
    estimated_completion_time = Column(String(255), nullable=True)
    proposed_start_date = Column(DateTime(timezone=True), nullable=True)
    experience_years = Column(Integer, nullable=True)
    portfolio_links = Column(Text, nullable=True)
    
    # Status and metadata
    status = Column(Enum(BidStatus), default=BidStatus.ACTIVE, index=True)
    is_automatic = Column(Boolean, default=False)  # For auto-bidding features
    
    # Foreign keys
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    auction = relationship("Auction", back_populates="bids", foreign_keys=[auction_id])
    bidder = relationship("User", back_populates="bids")
    
    def __repr__(self):
        return f"<Bid(id={self.id}, amount={self.amount}, auction_id={self.auction_id})>"

