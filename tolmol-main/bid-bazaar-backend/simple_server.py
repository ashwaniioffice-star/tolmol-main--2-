#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/v1/auctions')
def get_auctions():
    return jsonify([
        {
            'id': 1,
            'title': 'House Cleaning Service',
            'description': 'Need professional house cleaning for a 3BHK apartment.',
            'category': 'cleaning',
            'location': 'Bangalore, Karnataka',
            'starting_price': 1500.00,
            'current_lowest_bid': 1200.00,
            'status': 'active',
            'is_hot_deal': True,
            'is_active': True,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'title': 'Math Tutoring for Class 10',
            'description': 'Looking for experienced math tutor for CBSE Class 10 student.',
            'category': 'tutoring',
            'location': 'Delhi, India',
            'starting_price': 800.00,
            'current_lowest_bid': 600.00,
            'status': 'active',
            'is_hot_deal': False,
            'is_active': True,
            'created_at': '2024-01-02T00:00:00Z'
        },
        {
            'id': 3,
            'title': 'Logo Design for Startup',
            'description': 'Need a professional logo design for my tech startup.',
            'category': 'design',
            'location': 'Mumbai, Maharashtra',
            'starting_price': 3500.00,
            'current_lowest_bid': 2800.00,
            'status': 'active',
            'is_hot_deal': True,
            'is_active': True,
            'created_at': '2024-01-03T00:00:00Z'
        }
    ])

@app.route('/api/v1/login', methods=['POST'])
def login():
    return jsonify({
        'access_token': 'demo-token-123',
        'token_type': 'bearer',
        'user': {
            'id': 1,
            'username': 'demo',
            'email': 'demo@example.com'
        }
    })

@app.route('/api/v1/register', methods=['POST'])
def register():
    return jsonify({
        'access_token': 'demo-token-456',
        'token_type': 'bearer',
        'user': {
            'id': 2,
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
    })

if __name__ == '__main__':
    print("Starting Bid Bazaar Backend Server...")
    print("Server will be available at: http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)

