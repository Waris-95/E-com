from market import app
from flask import render_template
from market.models import Item

# home route
@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

# shop route
@app.route('/shop')
def shop_page():
    items = Item.query.all()
    return render_template('market.html', items=items)