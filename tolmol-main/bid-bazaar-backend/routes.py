from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Auction, Bid
from forms import RegistrationForm, LoginForm, AuctionForm, BidForm
from datetime import datetime
from sqlalchemy import or_, desc

@app.route('/')
def index():
    # Get search and filter parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    
    # Base query for active auctions
    query = Auction.query.filter(
        Auction.is_active == True,
        Auction.end_time > datetime.utcnow()
    )
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Auction.title.contains(search),
                Auction.description.contains(search)
            )
        )
    
    if category:
        query = query.filter(Auction.category == category)
    
    if location:
        query = query.filter(Auction.location.contains(location))
    
    # Order by creation time (newest first)
    auctions = query.order_by(desc(Auction.created_at)).all()
    
    # Get categories for filter dropdown
    categories = [
        ('home_repair', 'Home Repair'),
        ('cleaning', 'Cleaning'),
        ('tutoring', 'Tutoring'),
        ('delivery', 'Delivery'),
        ('design', 'Design & Creative'),
        ('tech_support', 'Tech Support'),
        ('beauty', 'Beauty & Wellness'),
        ('automotive', 'Automotive'),
        ('other', 'Other')
    ]
    
    return render_template('index.html', auctions=auctions, categories=categories,
                         search=search, selected_category=category, selected_location=location)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            is_service_provider=form.is_service_provider.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's auctions if they're a service provider
    my_auctions = []
    if current_user.is_service_provider:
        my_auctions = Auction.query.filter_by(creator_id=current_user.id).order_by(desc(Auction.created_at)).all()
    
    # Get user's bids
    my_bids = db.session.query(Bid, Auction).join(Auction).filter(
        Bid.bidder_id == current_user.id
    ).order_by(desc(Bid.created_at)).all()
    
    return render_template('dashboard.html', my_auctions=my_auctions, my_bids=my_bids)

@app.route('/create_auction', methods=['GET', 'POST'])
@login_required
def create_auction():
    if not current_user.is_service_provider:
        flash('Only service providers can create auctions.', 'warning')
        return redirect(url_for('index'))
    
    form = AuctionForm()
    if form.validate_on_submit():
        # Determine radius based on location type
        radius_map = {'local': 10, 'city': 50, 'state': 500}
        radius = radius_map.get(form.location_type.data, 50)
        
        auction = Auction(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            location=form.location.data,
            starting_bid=form.starting_bid.data,
            end_time=form.end_time.data,
            creator_id=current_user.id,
            location_type=form.location_type.data,
            city=form.city.data,
            state=form.state.data,
            radius_km=radius
        )
        db.session.add(auction)
        db.session.commit()
        flash('Auction created successfully with GPS location!', 'success')
        return redirect(url_for('auction_detail', auction_id=auction.id))
    
    return render_template('create_auction.html', form=form)

@app.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    
    # Get bid history
    bids = Bid.query.filter_by(auction_id=auction_id).order_by(desc(Bid.created_at)).all()
    
    # Create bid form for logged-in users
    bid_form = BidForm() if current_user.is_authenticated else None
    
    return render_template('auction_detail.html', auction=auction, bids=bids, bid_form=bid_form)

@app.route('/place_bid/<int:auction_id>', methods=['POST'])
@login_required
def place_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    
    # Check if auction is still active
    if auction.is_expired or not auction.is_active:
        flash('This auction has ended.', 'warning')
        return redirect(url_for('auction_detail', auction_id=auction_id))
    
    # Check if user is trying to bid on their own auction
    if auction.creator_id == current_user.id:
        flash('You cannot bid on your own auction.', 'warning')
        return redirect(url_for('auction_detail', auction_id=auction_id))
    
    form = BidForm()
    if form.validate_on_submit():
        bid_amount = form.amount.data
        current_lowest = auction.get_lowest_bid()
        
        # Validate bid amount (must be lower than current bid in reverse auction)
        if bid_amount >= current_lowest:
            flash(f'Your bid must be lower than the current bid of ₹{current_lowest:.2f}', 'warning')
            return redirect(url_for('auction_detail', auction_id=auction_id))
        
        # Create new bid
        bid = Bid(
            amount=bid_amount,
            auction_id=auction_id,
            bidder_id=current_user.id
        )
        
        # Update auction's current bid
        auction.current_bid = bid_amount
        
        db.session.add(bid)
        db.session.commit()
        
        flash('Bid placed successfully!', 'success')
        
        # Emit socket event for real-time update
        from app import socketio
        socketio.emit('new_bid', {
            'auction_id': auction_id,
            'amount': bid_amount,
            'bidder': 'Anonymous',
            'timestamp': bid.created_at.strftime('%H:%M:%S')
        }, room=f'auction_{auction_id}')
        
    return redirect(url_for('auction_detail', auction_id=auction_id))

@app.route('/api/auction/<int:auction_id>/status')
def auction_status(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    return jsonify({
        'current_bid': auction.get_lowest_bid(),
        'time_remaining': auction.time_remaining.total_seconds() if not auction.is_expired else 0,
        'is_active': auction.is_active and not auction.is_expired
    })
