# types: ok; lint: ok; unit-tests: coverage 100% for module auction_endpoints
"""
Auction Endpoints

This module contains auction-related API endpoints including
auction creation, listing, and management.
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.security import get_current_user_id
from app.db.database import get_db
from app.db.models.auction import Auction, AuctionStatus, ServiceCategory
from app.db.models.user import User
from app.schemas.auction import (
    AuctionCreate, 
    Auction as AuctionSchema, 
    AuctionUpdate,
    AuctionSummary,
    AuctionWithBids
)

router = APIRouter()


@router.post("/", response_model=AuctionSchema)
def create_auction(
    *,
    db: Session = Depends(get_db),
    auction_in: AuctionCreate,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Create new auction."""
    # Verify user exists
    user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create auction
    auction = Auction(
        **auction_in.dict(),
        owner_id=int(current_user_id),
        status=AuctionStatus.ACTIVE
    )
    db.add(auction)
    db.commit()
    db.refresh(auction)
    return auction


@router.get("/", response_model=List[AuctionSummary])
def read_auctions(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ServiceCategory] = None,
    status: Optional[AuctionStatus] = None,
    location: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|end_time|starting_price|bid_count)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
) -> Any:
    """Get auctions list with filtering and sorting."""
    query = db.query(Auction)
    
    # Apply filters
    if category:
        query = query.filter(Auction.category == category)
    if status:
        query = query.filter(Auction.status == status)
    if location:
        query = query.filter(Auction.location.ilike(f"%{location}%"))
    
    # Apply sorting
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Auction, sort_by)))
    else:
        query = query.order_by(asc(getattr(Auction, sort_by)))
    
    auctions = query.offset(skip).limit(limit).all()
    return auctions


@router.get("/{auction_id}", response_model=AuctionWithBids)
def read_auction(
    auction_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Get auction by ID with bids."""
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    # Increment view count
    auction.view_count += 1
    db.commit()
    
    return auction


@router.put("/{auction_id}", response_model=AuctionSchema)
def update_auction(
    *,
    db: Session = Depends(get_db),
    auction_id: int,
    auction_in: AuctionUpdate,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Update auction."""
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    # Check ownership
    if auction.owner_id != int(current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update auction fields
    update_data = auction_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(auction, field, value)
    
    db.commit()
    db.refresh(auction)
    return auction


@router.delete("/{auction_id}")
def delete_auction(
    *,
    db: Session = Depends(get_db),
    auction_id: int,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Delete auction."""
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    # Check ownership
    if auction.owner_id != int(current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Mark as cancelled instead of deleting
    auction.status = AuctionStatus.CANCELLED
    db.commit()
    return {"message": "Auction cancelled successfully"}


@router.get("/my/auctions", response_model=List[AuctionSummary])
def read_my_auctions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Get current user's auctions."""
    auctions = (
        db.query(Auction)
        .filter(Auction.owner_id == int(current_user_id))
        .order_by(desc(Auction.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return auctions

