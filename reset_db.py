from market import db
from market.models import User, Item

db.drop_all()  # This will drop all tables
db.create_all()  # Recreate all tables without any data
