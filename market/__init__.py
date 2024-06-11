from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database configuration for development and production
if os.getenv('FLASK_ENV') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    app.config['DEBUG'] = True  # Add this line to enable debugging
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['DEBUG'] = True  # Add this line to enable debugging

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from market.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

# to render a better 401
@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.before_request
def set_schema():
    if 'sqlite' not in app.config['SQLALCHEMY_DATABASE_URI']:
        schema = os.getenv('SCHEMA')
        if schema:
            with db.engine.connect() as connection:
                connection.execute(text(f'SET search_path TO {schema};'))

# Import routes after initializing app, db, and other components to avoid circular import
from market import routes

# Register commands
from market.seed import seed
app.cli.add_command(seed)
