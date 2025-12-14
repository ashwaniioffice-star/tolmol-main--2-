from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Auction, Bid
from datetime import datetime
from sqlalchemy import or_, desc
import logging

# API Routes for Frontend Integration

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data.get('phone', ''),
            is_service_provider=data.get('is_service_provider', False)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_service_provider': user.is_service_provider
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_service_provider': user.is_service_provider
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/auth/me', methods=['GET'])
@login_required
def api_current_user():
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'is_service_provider': current_user.is_service_provider
        }
    }), 200



@app.route('/api/auctions', methods=['GET'])
def api_get_auctions():
    try:
        # Get query parameters
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        location = request.args.get('location', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
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
        
        # Paginate results
        auctions = query.order_by(desc(Auction.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        auction_list = []
        for auction in auctions.items:
            auction_data = {
                'id': auction.id,
                'title': auction.title,
                'description': auction.description,
                'category': auction.category,
                'location': auction.location,
                'starting_bid': auction.starting_bid,
                'current_bid': auction.current_bid,
                'end_time': auction.end_time.isoformat(),
                'is_active': auction.is_active,
                'is_hot_deal': auction.is_hot_deal,
                'created_at': auction.created_at.isoformat(),
                'creator': {
                    'username': auction.creator.username,
                    'email': auction.creator.email
                },
                'creator_id': auction.creator_id,
                'time_remaining': auction.time_remaining.total_seconds() if not auction.is_expired else 0,
                'lowest_bid': auction.get_lowest_bid(),
                'bids': []  # Will be populated if needed
            }
            auction_list.append(auction_data)
        
        return jsonify({
            'auctions': auction_list,
            'pagination': {
                'page': auctions.page,
                'pages': auctions.pages,
                'per_page': auctions.per_page,
                'total': auctions.total,
                'has_next': auctions.has_next,
                'has_prev': auctions.has_prev
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Get auctions error: {str(e)}")
        return jsonify({'error': 'Failed to fetch auctions'}), 500

@app.route('/api/auctions', methods=['POST'])
@login_required
def api_create_auction():
    try:
        if not current_user.is_service_provider:
            return jsonify({'error': 'Only service providers can create auctions'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'location', 'starting_bid', 'end_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Parse end_time
        try:
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid end_time format'}), 400
        
        # Validate end_time is in the future
        if end_time <= datetime.utcnow():
            return jsonify({'error': 'End time must be in the future'}), 400
        
        # Determine radius based on location type
        radius_map = {'local': 10, 'city': 50, 'state': 500}
        location_type = data.get('location_type', 'city')
        radius = radius_map.get(location_type, 50)
        
        # Create auction
        auction = Auction(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            location=data['location'],
            starting_bid=float(data['starting_bid']),
            end_time=end_time,
            creator_id=current_user.id,
            location_type=location_type,
            city=data.get('city', ''),
            state=data.get('state', ''),
            radius_km=radius
        )
        
        db.session.add(auction)
        db.session.commit()
        
        return jsonify({
            'message': 'Auction created successfully',
            'auction': {
                'id': auction.id,
                'title': auction.title,
                'description': auction.description,
                'category': auction.category,
                'location': auction.location,
                'starting_bid': auction.starting_bid,
                'end_time': auction.end_time.isoformat(),
                'creator': auction.creator.username
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Create auction error: {str(e)}")
        return jsonify({'error': 'Failed to create auction'}), 500


@app.route('/api/auctions/<int:auction_id>', methods=['GET'])
def api_get_auction(auction_id):
    try:
        auction = Auction.query.get_or_404(auction_id)
        
        # Get bid history
        bids = Bid.query.filter_by(auction_id=auction_id).order_by(desc(Bid.created_at)).all()
        
        bid_list = []
        for bid in bids:
            bid_data = {
                'id': bid.id,
                'amount': bid.amount,
                'created_at': bid.created_at.isoformat(),
                'bidder': 'Anonymous'  # Keep bidder anonymous for privacy
            }
            bid_list.append(bid_data)
        
        auction_data = {
            'id': auction.id,
            'title': auction.title,
            'description': auction.description,
            'category': auction.category,
            'location': auction.location,
            'starting_bid': auction.starting_bid,
            'current_bid': auction.current_bid,
            'end_time': auction.end_time.isoformat(),
            'is_active': auction.is_active,
            'is_hot_deal': auction.is_hot_deal,
            'created_at': auction.created_at.isoformat(),
            'creator': {
                'username': auction.creator.username,
                'email': auction.creator.email
            },
            'creator_id': auction.creator_id,
            'time_remaining': auction.time_remaining.total_seconds() if not auction.is_expired else 0,
            'lowest_bid': auction.get_lowest_bid(),
            'bids': bid_list
        }
        
        return jsonify({'auction': auction_data}), 200
        
    except Exception as e:
        logging.error(f"Get auction error: {str(e)}")
        return jsonify({'error': 'Failed to fetch auction'}), 500

@app.route('/api/auctions/<int:auction_id>/bid', methods=['POST'])
@login_required
def api_place_bid(auction_id):
    try:
        auction = Auction.query.get_or_404(auction_id)
        
        # Check if auction is still active
        if auction.is_expired or not auction.is_active:
            return jsonify({'error': 'This auction has ended'}), 400
        
        # Check if user is trying to bid on their own auction
        if auction.creator_id == current_user.id:
            return jsonify({'error': 'You cannot bid on your own auction'}), 400
        
        data = request.get_json()
        bid_amount = float(data.get('amount', 0))
        
        if bid_amount <= 0:
            return jsonify({'error': 'Bid amount must be positive'}), 400
        
        current_lowest = auction.get_lowest_bid()
        
        # Validate bid amount (must be lower than current bid in reverse auction)
        if bid_amount >= current_lowest:
            return jsonify({'error': f'Your bid must be lower than the current bid of ₹{current_lowest:.2f}'}), 400
        
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
        
        # Emit socket event for real-time update
        from app import socketio
        socketio.emit('new_bid', {
            'auction_id': auction_id,
            'amount': bid_amount,
            'bidder': 'Anonymous',
            'timestamp': bid.created_at.strftime('%H:%M:%S')
        }, room=f'auction_{auction_id}')
        
        return jsonify({
            'message': 'Bid placed successfully',
            'bid': {
                'id': bid.id,
                'amount': bid.amount,
                'created_at': bid.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Place bid error: {str(e)}")
        return jsonify({'error': 'Failed to place bid'}), 500

@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    try:
        # Get user's auctions if they're a service provider
        my_auctions = []
        if current_user.is_service_provider:
            auctions = Auction.query.filter_by(creator_id=current_user.id).order_by(desc(Auction.created_at)).all()
            for auction in auctions:
                auction_data = {
                    'id': auction.id,
                    'title': auction.title,
                    'category': auction.category,
                    'starting_bid': auction.starting_bid,
                    'current_bid': auction.current_bid,
                    'end_time': auction.end_time.isoformat(),
                    'is_active': auction.is_active,
                    'time_remaining': auction.time_remaining.total_seconds() if not auction.is_expired else 0,
                    'bid_count': len(auction.bids)
                }
                my_auctions.append(auction_data)
        
        # Get user's bids
        my_bids = []
        bids = db.session.query(Bid, Auction).join(Auction).filter(
            Bid.bidder_id == current_user.id
        ).order_by(desc(Bid.created_at)).all()
        
        for bid, auction in bids:
            bid_data = {
                'id': bid.id,
                'amount': bid.amount,
                'created_at': bid.created_at.isoformat(),
                'auction': {
                    'id': auction.id,
                    'title': auction.title,
                    'category': auction.category,
                    'end_time': auction.end_time.isoformat(),
                    'is_active': auction.is_active,
                    'current_bid': auction.current_bid
                }
            }
            my_bids.append(bid_data)
        
        return jsonify({
            'my_auctions': my_auctions,
            'my_bids': my_bids
        }), 200
        
    except Exception as e:
        logging.error(f"Dashboard error: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    categories = [
        {'value': 'home_repair', 'label': 'Home Repair'},
        {'value': 'cleaning', 'label': 'Cleaning'},
        {'value': 'tutoring', 'label': 'Tutoring'},
        {'value': 'delivery', 'label': 'Delivery'},
        {'value': 'design', 'label': 'Design & Creative'},
        {'value': 'tech_support', 'label': 'Tech Support'},
        {'value': 'beauty', 'label': 'Beauty & Wellness'},
        {'value': 'automotive', 'label': 'Automotive'},
        {'value': 'other', 'label': 'Other'}
    ]
    return jsonify({'categories': categories}), 200

@app.route('/api/states', methods=['GET'])
def api_get_states():
    states = [
        {'value': 'andhra-pradesh', 'label': 'Andhra Pradesh'},
        {'value': 'arunachal-pradesh', 'label': 'Arunachal Pradesh'},
        {'value': 'assam', 'label': 'Assam'},
        {'value': 'bihar', 'label': 'Bihar'},
        {'value': 'chhattisgarh', 'label': 'Chhattisgarh'},
        {'value': 'goa', 'label': 'Goa'},
        {'value': 'gujarat', 'label': 'Gujarat'},
        {'value': 'haryana', 'label': 'Haryana'},
        {'value': 'himachal-pradesh', 'label': 'Himachal Pradesh'},
        {'value': 'jharkhand', 'label': 'Jharkhand'},
        {'value': 'karnataka', 'label': 'Karnataka'},
        {'value': 'kerala', 'label': 'Kerala'},
        {'value': 'madhya-pradesh', 'label': 'Madhya Pradesh'},
        {'value': 'maharashtra', 'label': 'Maharashtra'},
        {'value': 'manipur', 'label': 'Manipur'},
        {'value': 'meghalaya', 'label': 'Meghalaya'},
        {'value': 'mizoram', 'label': 'Mizoram'},
        {'value': 'nagaland', 'label': 'Nagaland'},
        {'value': 'odisha', 'label': 'Odisha'},
        {'value': 'punjab', 'label': 'Punjab'},
        {'value': 'rajasthan', 'label': 'Rajasthan'},
        {'value': 'sikkim', 'label': 'Sikkim'},
        {'value': 'tamil-nadu', 'label': 'Tamil Nadu'},
        {'value': 'telangana', 'label': 'Telangana'},
        {'value': 'tripura', 'label': 'Tripura'},
        {'value': 'uttar-pradesh', 'label': 'Uttar Pradesh'},
        {'value': 'uttarakhand', 'label': 'Uttarakhand'},
        {'value': 'west-bengal', 'label': 'West Bengal'},
        {'value': 'delhi', 'label': 'Delhi'},
        {'value': 'mumbai', 'label': 'Mumbai'},
        {'value': 'kolkata', 'label': 'Kolkata'},
        {'value': 'chennai', 'label': 'Chennai'}
    ]
    return jsonify({'states': states}), 200

