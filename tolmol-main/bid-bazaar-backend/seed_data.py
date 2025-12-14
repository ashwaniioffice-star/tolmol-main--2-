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
        
        # Create sample auctions
        auctions_data = [
            {
                "title": "Logo Design for Startup",
                "description": "Need a modern, Gen-Z friendly logo for my new app. Looking for minimalist design with bold colors. Should work well on mobile screens.",
                "category": "design",
                "location": "Mumbai, MH",
                "starting_bid": 5000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(hours=2)
            },
            {
                "title": "Deep Clean My 2BHK Apartment",
                "description": "Moving in next week, need professional deep cleaning service. Kitchen, bathrooms, all rooms. Should use eco-friendly products.",
                "category": "cleaning",
                "location": "Bangalore, KA",
                "starting_bid": 3500.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(hours=4)
            },
            {
                "title": "Wedding Photography Package",
                "description": "Looking for candid wedding photography for Dec 2025 wedding. Need pre-wedding, ceremony, and reception coverage. 300+ edited photos required.",
                "category": "other",
                "location": "Delhi, DL",
                "starting_bid": 25000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(hours=6)
            },
            {
                "title": "Python Tutoring - 10 Sessions",
                "description": "Need help learning Python for data science. Complete beginner, prefer online classes on weekends. Looking for structured curriculum.",
                "category": "tutoring",
                "location": "Pune, MH",
                "starting_bid": 8000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(hours=8)
            },
            {
                "title": "Bulk Delivery - 100 Parcels",
                "description": "Need same-day delivery for 100 small parcels across the city. All addresses within 20km radius. Professional handling required.",
                "category": "delivery",
                "location": "Chennai, TN",
                "starting_bid": 12000.00,
                "is_hot_deal": False,
                "end_time": datetime.utcnow() + timedelta(hours=12)
            },
            {
                "title": "Mobile App Development - Food Delivery",
                "description": "Build a simple food delivery app like Zomato. Need iOS and Android versions. Basic features: menu, cart, payment, tracking.",
                "category": "tech_support",
                "location": "Hyderabad, TG",
                "starting_bid": 150000.00,
                "is_hot_deal": True,
                "end_time": datetime.utcnow() + timedelta(days=1)
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
                creator_id=user1.id  # User1 creates all auctions
            )
            db.session.add(auction)
        
        db.session.commit()
        print("✅ Created 6 sample auctions")
        
        print("\n🎯 Sample login credentials:")
        print("Service Provider: designpro / password123")
        print("Regular User: dealhunter / password123") 
        print("\n🚀 BidBaazr is ready to roll!")

if __name__ == "__main__":
    create_sample_data()