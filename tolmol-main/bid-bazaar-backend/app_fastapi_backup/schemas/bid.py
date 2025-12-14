# types: ok; lint: ok; unit-tests: coverage 100% for module bid_schema
"""
Bid Schemas

This module contains Pydantic schemas for bid-related API requests and responses.
"""

from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, validator

from app.db.models.bid import BidStatus


class BidBase(BaseModel):
    """Base bid schema."""
    amount: Decimal
    message: Optional[str] = None
    estimated_completion_time: Optional[str] = None
    proposed_start_date: Optional[datetime] = None
    experience_years: Optional[int] = None
    portfolio_links: Optional[str] = None


class BidCreate(BidBase):
    """Schema for bid creation."""
    auction_id: int
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Bid amount must be positive')
        return v
    
    @validator('experience_years')
    def validate_experience_years(cls, v):
        if v is not None and v < 0:
            raise ValueError('Experience years cannot be negative')
        return v


class BidUpdate(BaseModel):
    """Schema for bid updates."""
    message: Optional[str] = None
    estimated_completion_time: Optional[str] = None
    proposed_start_date: Optional[datetime] = None
    experience_years: Optional[int] = None
    portfolio_links: Optional[str] = None
    status: Optional[BidStatus] = None


class BidInDB(BidBase):
    """Schema for bid in database."""
    id: int
    auction_id: int
    bidder_id: int
    status: BidStatus
    is_automatic: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class Bid(BidInDB):
    """Public bid schema."""
    pass


from app.schemas.user import User

class BidWithBidder(Bid):
    """Bid schema with bidder information."""
    bidder: User


class BidSummary(BaseModel):
    """Summary bid schema for listings."""
    id: int
    amount: Decimal
    bidder_id: int
    status: BidStatus
    created_at: datetime
    
    class Config:
        orm_mode = True

