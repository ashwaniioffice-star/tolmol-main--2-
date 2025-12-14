from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio
import logging

@socketio.on('connect')
def handle_connect():
    logging.info(f'Client connected: {current_user.username if current_user.is_authenticated else "Anonymous"}')

@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f'Client disconnected: {current_user.username if current_user.is_authenticated else "Anonymous"}')

@socketio.on('join_auction')
def handle_join_auction(data):
    auction_id = data['auction_id']
    room = f'auction_{auction_id}'
    join_room(room)
    emit('status', {'msg': f'Joined auction {auction_id} room'})
    logging.info(f'User joined auction {auction_id} room')

@socketio.on('leave_auction')
def handle_leave_auction(data):
    auction_id = data['auction_id']
    room = f'auction_{auction_id}'
    leave_room(room)
    emit('status', {'msg': f'Left auction {auction_id} room'})
    logging.info(f'User left auction {auction_id} room')

@socketio.on('request_auction_update')
def handle_auction_update(data):
    auction_id = data['auction_id']
    from models import Auction
    auction = Auction.query.get(auction_id)
    
    if auction:
        emit('auction_update', {
            'current_bid': auction.get_lowest_bid(),
            'time_remaining': auction.time_remaining.total_seconds() if not auction.is_expired else 0,
            'is_active': auction.is_active and not auction.is_expired
        })
