from market import app
from flask import render_template, jsonify, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm
from market import db

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

# route for signup
@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('shop_page'))
    if form.errors != {}:  # if there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', 'danger')
    return render_template('register.html', form=form)
