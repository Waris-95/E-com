from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    from market.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

# to render a better 401
@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

from market import routes  # Import here to avoid circular import

# Register commands
from market.seed import seed
app.cli.add_command(seed)

@app.before_first_request
def set_schema():
    schema = os.getenv('SCHEMA')
    if schema:
        db.engine.execute(f'SET search_path TO {schema};')