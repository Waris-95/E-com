from market import app
from flask import render_template, jsonify
from market.models import Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/shop')
def shop_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

# route to display items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'name': item.name, 'price': item.price, 'barcode': item.barcode, 'description': item.description} for item in items]
    return jsonify(items_list)