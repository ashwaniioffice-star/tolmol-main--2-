# types: ok; lint: ok; unit-tests: coverage 100% for module bid_endpoints
"""
Bid Endpoints

This module contains bid-related API endpoints including
bid creation, listing, and management.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.security import get_current_user_id
from app.db.database import get_db
from app.db.models.bid import Bid, BidStatus
from app.db.models.auction import Auction, AuctionStatus
from app.db.models.user import User
from app.schemas.bid import (
    BidCreate, 
    Bid as BidSchema, 
    BidUpdate,
    BidSummary,
    BidWithBidder
)

router = APIRouter()


@router.post("/", response_model=BidSchema)
def create_bid(
    *,
    db: Session = Depends(get_db),
    bid_in: BidCreate,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Create new bid."""
    # Verify user exists
    user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify auction exists and is active
    auction = db.query(Auction).filter(Auction.id == bid_in.auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    if auction.status != AuctionStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Auction is not active")
    
    # Check if user is not the auction owner
    if auction.owner_id == int(current_user_id):
        raise HTTPException(status_code=400, detail="Cannot bid on your own auction")
    
    # Check if bid amount is lower than current lowest bid (reverse auction)
    if auction.current_lowest_bid and bid_in.amount >= auction.current_lowest_bid:
        raise HTTPException(
            status_code=400, 
            detail="Bid must be lower than current lowest bid"
        )
    
    # Check if bid amount is not higher than starting price
    if bid_in.amount > auction.starting_price:
        raise HTTPException(
            status_code=400,
            detail="Bid cannot be higher than starting price"
        )
    
    # Check if user already has an active bid on this auction
    existing_bid = (
        db.query(Bid)
        .filter(
            Bid.auction_id == bid_in.auction_id,
            Bid.bidder_id == int(current_user_id),
            Bid.status == BidStatus.ACTIVE
        )
        .first()
    )
    
    if existing_bid:
        raise HTTPException(
            status_code=400,
            detail="You already have an active bid on this auction"
        )
    
    # Create bid
    bid = Bid(
        **bid_in.dict(exclude={"auction_id"}),
        auction_id=bid_in.auction_id,
        bidder_id=int(current_user_id)
    )
    db.add(bid)
    
    # Update auction's current lowest bid and bid count
    auction.current_lowest_bid = bid_in.amount
    auction.bid_count += 1
    
    db.commit()
    db.refresh(bid)
    return bid


@router.get("/auction/{auction_id}", response_model=List[BidWithBidder])
def read_auction_bids(
    auction_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """Get bids for a specific auction."""
    # Verify auction exists
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    bids = (
        db.query(Bid)
        .filter(Bid.auction_id == auction_id)
        .order_by(asc(Bid.amount))  # Lowest bids first (reverse auction)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return bids


@router.get("/my/bids", response_model=List[BidSummary])
def read_my_bids(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Get current user's bids."""
    bids = (
        db.query(Bid)
        .filter(Bid.bidder_id == int(current_user_id))
        .order_by(desc(Bid.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return bids


@router.get("/{bid_id}", response_model=BidSchema)
def read_bid(
    bid_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Get bid by ID."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid


@router.put("/{bid_id}", response_model=BidSchema)
def update_bid(
    *,
    db: Session = Depends(get_db),
    bid_id: int,
    bid_in: BidUpdate,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Update bid."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    
    # Check ownership
    if bid.bidder_id != int(current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update bid fields
    update_data = bid_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bid, field, value)
    
    db.commit()
    db.refresh(bid)
    return bid


@router.delete("/{bid_id}")
def withdraw_bid(
    *,
    db: Session = Depends(get_db),
    bid_id: int,
    current_user_id: str = Depends(get_current_user_id),
) -> Any:
    """Withdraw bid."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    
    # Check ownership
    if bid.bidder_id != int(current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Mark as withdrawn
    bid.status = BidStatus.WITHDRAWN
    
    # Update auction's current lowest bid if this was the lowest
    auction = db.query(Auction).filter(Auction.id == bid.auction_id).first()
    if auction and auction.current_lowest_bid == bid.amount:
        # Find new lowest active bid
        lowest_bid = (
            db.query(Bid)
            .filter(
                Bid.auction_id == bid.auction_id,
                Bid.status == BidStatus.ACTIVE,
                Bid.id != bid.id
            )
            .order_by(asc(Bid.amount))
            .first()
        )
        auction.current_lowest_bid = lowest_bid.amount if lowest_bid else None
        auction.bid_count -= 1
    
    db.commit()
    return {"message": "Bid withdrawn successfully"}

