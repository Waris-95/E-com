from market import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run()