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
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)   
                flash(f"Your order has been placed. An email will be sent when your order has been shipped.", category='success')
            else:
                flash(f"Unfortunately, you don't have enough budget for {p_item_object.name}", category='danger')
        # After handling POST request, redirect to GET to show updated item list
        return redirect(url_for('shop_page'))
    
    elif request.method == 'GET':
        items = Item.query.filter_by(owner=None).all()
        owned_items = Item.query.filter_by(owner=current_user.id).all()
        print(f"Owned Items: {owned_items}") 
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items)


# Route to display items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'name': item.name, 'price': item.price, 'barcode': item.barcode, 'description': item.description} for item in items]
    return jsonify(items_list)

# route to sell items
@app.route('/sell_item/<int:item_id>', methods=['POST'])
@login_required
def sell_item(item_id):
    item = Item.query.get(item_id)
    if item and item.owner == current_user.id:
        current_user.budget += item.price
        item.owner = None  # Remove ownership
        db.session.commit()
        flash(f'Successfully sold {item.name} for ${item.price}!', 'success')
    else:
        flash('Item not found or you do not own this item.', 'danger')
    return redirect(url_for('shop_page'))


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
