#!/usr/bin/env python3
"""
Seed data script for BidBaazr platform
Creates sample users and auctions to showcase the platform
"""

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Auction

def create_sample_data():
    with app.app_context():
        print("🚀 Creating sample data for BidBaazr...")
        
        # Create sample users
        # Service Provider 1
        provider1 = User(
            username="designpro",
            email="design@bidbazr.com",
            phone="+91-9876543210",
            is_service_provider=True
        )
        provider1.set_password("password123")
        db.session.add(provider1)
        
        # Service Provider 2  
        provider2 = User(
            username="cleanmaster",
            email="clean@bidbazr.com", 
            phone="+91-9876543211",
            is_service_provider=True
        )
        provider2.set_password("password123")
        db.session.add(provider2)
        
        # Regular User 1
        user1 = User(
            username="dealhunter",
            email="hunter@bidbazr.com",
            phone="+91-9876543212",
            is_service_provider=False
        )
        user1.set_password("password123")
        db.session.add(user1)
        
        # Regular User 2
        user2 = User(
            username="smartbuyer",
            email="smart@bidbazr.com",
            phone="+91-9876543213", 
            is_service_provider=False
        )
        user2.set_password("password123")
        db.session.add(user2)
        
        db.session.commit()
        print("✅ Created 4 sample users")
        
        # Create sample auctions with realistic data
        auctions_data = [
            {
                "title": "Professional House Cleaning - 3BHK Apartment",
                "description": "Need professional deep cleaning for a 3BHK apartment in Koramangala. Kitchen, bathrooms, and all rooms. Eco-friendly products preferred. Available this weekend.",
                "category": "cleaning",
                "location": "Koramangala, Bangalore",
                "starting_bid": 3000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(hours=24),
                "city": "Bangalore",
                "state": "karnataka",
                "location_type": "city",
                "radius_km": 50
            },
            {
                "title": "Math & Physics Tutoring - Class 12 CBSE",
                "description": "Looking for experienced tutor for Class 12 CBSE student. Need help with advanced mathematics and physics. Prefer home visits in Noida. 2-3 sessions per week.",
                "category": "tutoring",
                "location": "Sector 62, Noida",
                "starting_bid": 2000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(hours=48),
                "city": "Noida",
                "state": "uttar-pradesh",
                "location_type": "local",
                "radius_km": 10
            },
            {
                "title": "Logo & Brand Identity Design for Tech Startup",
                "description": "Need complete brand identity design for new fintech startup. Logo, color palette, typography, and brand guidelines. Modern, professional, and trustworthy feel. Deliverables: Logo variations, style guide, and brand book.",
                "category": "design",
                "location": "Pune, Maharashtra",
                "starting_bid": 15000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(hours=72),
                "city": "Pune",
                "state": "maharashtra",
                "location_type": "state",
                "radius_km": 500
            },
            {
                "title": "Home Repair - Plumbing & Electrical Work",
                "description": "Need comprehensive home repair service. Fix leaking pipes in kitchen and bathroom, install new electrical outlets in living room, and repair broken tiles. Professional work required with warranty.",
                "category": "home_repair",
                "location": "Andheri West, Mumbai",
                "starting_bid": 5000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(hours=36),
                "city": "Mumbai",
                "state": "maharashtra",
                "location_type": "city",
                "radius_km": 50
            },
            {
                "title": "Website Development - E-commerce Platform",
                "description": "Build a complete e-commerce website for fashion retail. Features needed: Product catalog, shopping cart, payment gateway integration, admin dashboard, and mobile responsive design. Tech stack: React/Next.js preferred.",
                "category": "tech_support",
                "location": "Gurgaon, Haryana",
                "starting_bid": 50000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(days=7),
                "city": "Gurgaon",
                "state": "haryana",
                "location_type": "state",
                "radius_km": 500
            },
            {
                "title": "Beauty & Spa Services - Wedding Package",
                "description": "Complete bridal beauty package for wedding day. Includes: Hair styling, makeup, mehendi, and pre-wedding facial. Need experienced beautician for home service in South Delhi. Date: Next month.",
                "category": "beauty",
                "location": "South Delhi",
                "starting_bid": 8000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(days=20),
                "city": "Delhi",
                "state": "delhi",
                "location_type": "city",
                "radius_km": 30
            },
            {
                "title": "Car Service & Maintenance - Annual Service",
                "description": "Complete annual service for Honda City 2020. Includes: Oil change, filter replacement, brake inspection, AC service, and general checkup. Need authorized service center or experienced mechanic.",
                "category": "automotive",
                "location": "Whitefield, Bangalore",
                "starting_bid": 3500.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(days=5),
                "city": "Bangalore",
                "state": "karnataka",
                "location_type": "local",
                "radius_km": 15
            },
            {
                "title": "Content Writing - Blog Articles (10 Articles)",
                "description": "Need 10 high-quality blog articles (1000 words each) on technology and business topics. SEO optimized, original content, and well-researched. Topics will be provided. Deadline: 2 weeks.",
                "category": "other",
                "location": "Remote/Online",
                "starting_bid": 8000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(days=10),
                "city": "Any",
                "state": "any",
                "location_type": "state",
                "radius_km": 1000
            }
        ]
        
        for auction_data in auctions_data:
            auction = Auction(
                title=auction_data["title"],
                description=auction_data["description"],
                category=auction_data["category"],
                location=auction_data["location"],
                starting_bid=auction_data["starting_bid"],
                is_hot_deal=auction_data["is_hot_deal"],
                end_time=auction_data["end_time"],
                creator_id=user1.id,  # User1 creates all auctions
                city=auction_data.get("city", ""),
                state=auction_data.get("state", ""),
                location_type=auction_data.get("location_type", "city"),
                radius_km=auction_data.get("radius_km", 50)
            )
            db.session.add(auction)
        
        db.session.commit()
        print("✅ Created 8 realistic sample auctions")
        
        print("\n🎯 Sample login credentials:")
        print("Service Provider: designpro / password123")
        print("Regular User: dealhunter / password123") 
        print("\n🚀 BidBaazr is ready to roll!")

if __name__ == "__main__":
    create_sample_data()