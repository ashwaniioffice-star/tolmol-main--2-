import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.environ.get("SESSION_SECRET", "dev_secret_key_change_in_production"))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for all routes
# Update this with your production frontend URL
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    os.environ.get("FRONTEND_URL", "")
]
# Filter out empty strings
allowed_origins = [origin for origin in allowed_origins if origin]
CORS(app, origins=allowed_origins if allowed_origins else "*", supports_credentials=True)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bidding_platform.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
}

# Initialize extensions
db = SQLAlchemy(app, model_class=Base)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    import models  # noqa: F401
    db.create_all()
    logging.info("Database tables created")
