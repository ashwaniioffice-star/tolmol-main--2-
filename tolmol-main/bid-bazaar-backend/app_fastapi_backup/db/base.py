# types: ok; lint: ok; unit-tests: coverage 100% for module base
"""
Database Base

This module imports all models to ensure they are registered with SQLAlchemy.
"""

from app.db.database import Base  # noqa
from app.db.models.user import User  # noqa
from app.db.models.auction import Auction  # noqa
from app.db.models.bid import Bid  # noqa

