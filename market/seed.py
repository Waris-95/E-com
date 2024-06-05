import click
from flask.cli import with_appcontext
from market import db
from market.models import Item, User
from market import bcrypt

@click.command(name='seed')
@with_appcontext
def seed():
    # Create the database and the db tables
    db.create_all()

    # Clear existing records
    db.session.query(Item).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Insert seed data for users
    users = [
        User(username='user1', email_address='user1@example.com', password_hash=bcrypt.generate_password_hash('password1').decode('utf-8'), budget=1000),
        User(username='user2', email_address='user2@example.com', password_hash=bcrypt.generate_password_hash('password2').decode('utf-8'), budget=1500),
        User(username='user3', email_address='user3@example.com', password_hash=bcrypt.generate_password_hash('password3').decode('utf-8'), budget=2000),
    ]

    # Add all the users to the session
    for user in users:
        db.session.add(user)

    # Commit the session to the database
    db.session.commit()

    # Insert seed data for items
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

    print('Database seeded!')

# Ensure the app context is available when running the command
if __name__ == '__main__':
    with app.app_context():
        seed()
