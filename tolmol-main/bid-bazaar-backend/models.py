from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_service_provider = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    auctions = db.relationship('Auction', backref='creator', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    starting_bid = db.Column(db.Float, nullable=False)
    current_bid = db.Column(db.Float, nullable=True)
    end_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_hot_deal = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # GPS Location Fields
    location_type = db.Column(db.String(20), default='city')  # 'local', 'city', 'state'
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    radius_km = db.Column(db.Integer, default=50)  # Service radius in kilometers
    
    # Foreign key
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    bids = db.relationship('Bid', backref='auction', lazy=True, cascade='all, delete-orphan')

    @property
    def time_remaining(self):
        if self.end_time > datetime.utcnow():
            return self.end_time - datetime.utcnow()
        return timedelta(0)

    @property
    def is_expired(self):
        return datetime.utcnow() > self.end_time

    def get_lowest_bid(self):
        return self.current_bid or self.starting_bid

    def __repr__(self):
        return f'<Auction {self.title}>'

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Bid {self.amount} for auction {self.auction_id}>'
