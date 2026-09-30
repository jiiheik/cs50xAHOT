import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # fetch user id
    user_id = session["user_id"]

    # select stocks and cash
    stocks = db.execute("SELECT symbol, price, SUM(amount) as totalShares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # calculate total stocks
    total = cash

    for stock in stocks:
        total += stock["price"] * stock["totalShares"]

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # get symbol from form
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # check symbol and amount
        if not symbol:
            return apology("Error: no stock symbol given")
        elif not stock:
            return apology("Error: stock symbol does not exist")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Error: provide a valid amount")

        if shares <= 0:
            return apology("Error: amount needs to be more than 0")

        # check user id
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # set buy variables
        stock_name = stock["name"]
        stock_price = stock["price"]
        total_price = stock_price * shares

        # check amount of cash, execute if sufficient funds
        if cash < total_price:
            return apology("Error: insufficient funds")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            db.execute("INSERT INTO transactions (user_id, symbol, amount, price) VALUES (?, ?, ?, ?)",
                       user_id, symbol, shares, stock_price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # check user id
    user_id = session["user_id"]

    # Select transaction history
    transaction_history = db.execute("SELECT symbol, price, amount, transaction_time FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transaction_history=transaction_history, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get('symbol')

        # Check if no symbol given or invalid symbol, otherwise check symbol
        if not symbol:
            return apology("Error: no stock symbol given")

        stock = lookup(symbol)

        if not stock:
            return apology("Error: Stock symbol does not exist")

        return render_template("quoted.html", stock=stock, usd=usd)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pass
        # Get registration info
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # password validation
        if not username:
            return apology('Error: please give a username')
        elif not password:
            return apology('Error: please give a password')
        elif not confirmation:
            return apology('Error: please give your password again')
        elif password != confirmation:
            return apology('Error: passwords do not match')
        elif re.search('[0-9]', password) is None:
            return apology('Error: password needs to include at least one number')
        elif len(password) < 8:
            return apology('Error: password must have at least 8 characters')

        # hash password
        hash = generate_password_hash(password)

        # add user to table
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect('/')
        except:
            return apology('Error: username already in use')

    else:
        return render_template("register.html")
    """Register user"""


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # check amount of stocks
        if shares <= 0:
            return apology("Error: please set valid amount of stocks to be sold")

        stock_price = lookup(symbol)['price']
        stock_name = lookup(symbol)['symbol']

        owned_shares = db.execute("SELECT amount FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                  user_id, symbol)[0]["amount"]

        # check if enough shares to sell
        if owned_shares < shares:
            return apology("Error: not enough shares to sell")

        # check current cash amount
        cash_now = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        sold_price = shares * stock_price

        # update new cash amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash_now + sold_price), user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, amount, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, stock_price)

        return redirect("/")

    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)
