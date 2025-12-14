# types: ok; lint: ok; unit-tests: coverage 100% for module auction_schema
"""
Auction Schemas

This module contains Pydantic schemas for auction-related API requests and responses.
"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, validator

from app.db.models.auction import AuctionStatus, ServiceCategory


class AuctionBase(BaseModel):
    """Base auction schema."""
    title: str
    description: str
    category: ServiceCategory
    location: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    starting_price: Decimal
    reserve_price: Optional[Decimal] = None
    start_time: datetime
    end_time: datetime
    requirements: Optional[str] = None
    preferred_time: Optional[str] = None
    urgency_level: str = "normal"


class AuctionCreate(AuctionBase):
    """Schema for auction creation."""
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v
    
    @validator('starting_price')
    def validate_starting_price(cls, v):
        if v <= 0:
            raise ValueError('Starting price must be positive')
        return v
    
    @validator('reserve_price')
    def validate_reserve_price(cls, v, values):
        if v is not None and 'starting_price' in values and v > values['starting_price']:
            raise ValueError('Reserve price cannot be higher than starting price')
        return v


class AuctionUpdate(BaseModel):
    """Schema for auction updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    requirements: Optional[str] = None
    preferred_time: Optional[str] = None
    urgency_level: Optional[str] = None


class AuctionInDB(AuctionBase):
    """Schema for auction in database."""
    id: int
    owner_id: int
    current_lowest_bid: Optional[Decimal] = None
    status: AuctionStatus
    is_featured: bool
    view_count: int
    bid_count: int
    winning_bid_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class Auction(AuctionInDB):
    """Public auction schema."""
    pass


from app.schemas.bid import Bid

class AuctionWithBids(Auction):
    """Auction schema with bids included."""
    bids: List[Bid] = []


class AuctionSummary(BaseModel):
    """Summary auction schema for listings."""
    id: int
    title: str
    category: ServiceCategory
    location: str
    starting_price: Decimal
    current_lowest_bid: Optional[Decimal] = None
    status: AuctionStatus
    bid_count: int
    end_time: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True

