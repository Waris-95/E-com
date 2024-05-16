from flask import Flask, render_template

app = Flask(__name__)

# home route
@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

# shop route
@app.route('/shop')
def shop_page():
    return render_template('market.html')