from market import app, db
from market.models import Item

with app.app_context():
    # Create the database and the db table
    db.create_all()

    # Insert seed data
    items = [
        Item(name='Laptop', price=999, barcode='123456789012', description='A high-performance laptop.'),
        Item(name='Smartphone', price=499, barcode='123456789013', description='A latest model smartphone.'),
        Item(name='Headphones', price=199, barcode='123456789014', description='Noise-cancelling headphones.'),
        Item(name='Keyboard', price=49, barcode='123456789015', description='Mechanical keyboard with RGB lighting.'),
        Item(name='Mouse', price=29, barcode='123456789016', description='Wireless mouse with ergonomic design.')
    ]

    # Add all the items to the session
    for item in items:
        db.session.add(item)

    # Commit the session to the database
    db.session.commit()
