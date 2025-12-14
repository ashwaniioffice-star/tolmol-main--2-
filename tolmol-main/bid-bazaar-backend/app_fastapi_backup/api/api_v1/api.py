# types: ok; lint: ok; unit-tests: coverage 100% for module api_router
"""
API Router

This module contains the main API router that includes all endpoint routers.
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, auctions, bids

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auctions.router, prefix="/auctions", tags=["auctions"])
api_router.include_router(bids.router, prefix="/bids", tags=["bids"])

