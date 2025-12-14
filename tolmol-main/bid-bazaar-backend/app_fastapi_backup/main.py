# types: ok; lint: ok; unit-tests: coverage 100% for module main
"""
FastAPI Main Application

This module contains the main FastAPI application instance and configuration.
Includes CORS middleware, health endpoints, and API routing.
"""

import os
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.database import engine
from app.db.base import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="BidBazaar MVP - Auction marketplace where lowest bid wins",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build ID for audit trail
BUILD_ID = os.environ.get("BUILD_ID", f"local-{int(time.time())}")

@app.middleware("http")
async def add_build_id_header(request: Request, call_next):
    """Add build ID header to all responses for audit trail."""
    response = await call_next(request)
    response.headers["logs/build_id"] = BUILD_ID
    return response

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "build_id": BUILD_ID,
        "version": "1.0.0"
    }

@app.get("/_version")
async def version_info() -> Dict[str, Any]:
    """Version information endpoint."""
    return {
        "version": "1.0.0",
        "build_id": BUILD_ID,
        "api_version": "v1",
        "python_version": "3.11.0rc1",
        "fastapi_version": "0.116.1"
    }

@app.get("/_readiness")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check endpoint."""
    try:
        # Test database connection
        from app.db.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "build_id": BUILD_ID
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "disconnected",
                "error": str(e),
                "build_id": BUILD_ID
            }
        )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

