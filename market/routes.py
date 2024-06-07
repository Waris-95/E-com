from market import db, app
from flask import render_template, jsonify, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, login_required, current_user, logout_user

'''
------> Shop ROUTES <------
'''

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/shop', methods=['POST', 'GET'])
@login_required
def shop_page():
    purchase_form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            p_item_object.owner = current_user.id
            current_user.budget -= p_item_object.price
            db.session.commit()
            flash(f"your Order has been placed, an email will be sent upon dispatching {p_item_object.name} ")
    items = Item.query.filter_by(owner=None)
    
    return render_template('market.html', items=items, purchase_form=purchase_form)

# Route to display items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'name': item.name, 'price': item.price, 'barcode': item.barcode, 'description': item.description} for item in items]
    return jsonify(items_list)

'''
------> AUTH ROUTES <------
'''

# Route for signup
@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! Now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('shop_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', 'danger')
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Successfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('shop_page'))
        else:
            flash('Incorrect username or password', category='danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))
