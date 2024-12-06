import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
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
    # query db for username
    portfolio = db.execute(
        "SELECT stock, symbol, price, shares FROM portfolio WHERE userID = ?", session["id"])
    grandtotal = 0

    if not portfolio:
        db.execute("UPDATE users SET cash = 10000 WHERE id = ?", session["id"])

        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["id"])[
                     0]["cash"])  # Set cash to 10000 since you just updated it
        grandtotal = float(grandtotal)
        grandtotal += cash

        return render_template("index.html", cash=cash,  grandtotal=grandtotal)

    else:
        # get current price of stocks
        for stock in portfolio:
            shares = int(stock["shares"])
            stockdata = lookup(stock["symbol"])
            stock["price"] = float(stockdata["price"])
            stock["holdings"] = float(stockdata["price"] * shares)
            grandtotal += stock["holdings"]

        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["id"])[0]["cash"])
        grandtotal = float(grandtotal)
        grandtotal += cash

        return render_template("index.html", portfolio=portfolio, cash=cash, grandtotal=grandtotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("invalid symbol", 400)

        buystock = lookup(symbol)
        if not buystock:  # validate symbol input
            return apology("invalid symbol", 400)

        sharesinput = request.form.get("shares")

        if not sharesinput.isdigit():
            return apology("invalid number of shares", 400)

        shares = int(sharesinput)

        if shares < 1:  # valid shares input
            return apology("invalid number of shares", 400)

        price = float(buystock["price"])  # retrieve stock price

        # Calculate holdings
        holdings = price * shares
        holdings = float(holdings)

        # Ensure cash is a float
        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["id"])[0]["cash"])

        if cash > holdings:  # check there is enough money

            # query portfolio table for row with this userid and stock symbol:
            portfolio = db.execute(
                "SELECT * FROM portfolio WHERE userID = ? AND symbol = ?", session["id"], symbol)

            if len(portfolio) == 0:
                # add stock to user portfolio
                db.execute("INSERT INTO portfolio (stock, symbol, price, shares, holdings, userID) VALUES (?, ?, ?, ?, ?, ?)",
                           buystock["name"], buystock["symbol"], price, shares, holdings, session["id"])

            try:
                owned = int(db.execute(
                    "SELECT shares FROM portfolio WHERE userid = ? AND symbol = ?", session["id"], symbol)[0]["shares"])
            except:
                owned = 0

            updatedshares = owned + shares

            # update shares in portfolio table
            db.execute("UPDATE portfolio SET shares = ? WHERE userID = ? AND symbol = ?",
                       updatedshares, session["id"], symbol)
            db.execute("UPDATE portfolio SET holdings = ? WHERE userID = ? AND symbol = ?",
                       holdings, session["id"], symbol)

            # update user's cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", holdings, session["id"])
            cash = float(db.execute("SELECT cash FROM users WHERE id = ?",
                         session["id"])[0]["cash"])

            flash(f"Bought {shares} of {symbol} for {usd(holdings)}, cash balance: {usd(cash)}")

        else:
            return apology("insufficient funds", 402)

        # redirect user to home page
        return redirect("/")


@app.route("/history")
@login_required
def history():

    portfolio = db.execute(
        "SELECT transactionID, stock, symbol, price, shares, holdings, time FROM portfolio WHERE userID = ?", session["id"])

    for stock in portfolio:
        shares = int(stock["shares"])
        stockdata = lookup(stock["symbol"])
        stock["price"] = float(stockdata["price"])
        stock["holdings"] = float(stockdata["price"] * shares)
        stock["action"] = "BOUGHT" if stock["holdings"] > 0 else "SOLD"

    return render_template("history.html", portfolio=portfolio)


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
        session["id"] = rows[0]["id"]

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
        symbol = request.form.get("symbol")
        quote = lookup(symbol)  # retrieve stock quote

        if not quote:
            return apology("invalid symbol", 400)

        else:
            quoteprice = usd(quote["price"])
            # display stock quote
            return render_template("quoted.html", stock=quote, price=quoteprice)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password == "" or confirmation == "" or username == "":
            return apology("missing field", 400)

        if password != confirmation:
            return apology("password and confirmation don't match", 400)

        taken = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(taken) >= 1:
            return apology("username already taken", 400)
        else:
            hash = generate_password_hash(password)
            result = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            session["id"] = result
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # query db for user's stocks
    portfolio = db.execute("SELECT * FROM portfolio WHERE userID = ?", session["id"])

    # pick stock and number of shares
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:  # validate symbol input
            return apology("no holdings", 400)

        sellstock = lookup(symbol)
        heldshares = db.execute("SELECT SUM(shares) AS heldshares FROM portfolio WHERE symbol = ? AND userID = ?",
                                sellstock["symbol"], session["id"])[0]["heldshares"]
        shares = int(request.form.get("shares"))

        if shares <= 0:  # valid shares input
            return apology("invalid number of shares", 400)
        if shares > heldshares:
            return apology("insufficient shares owned", 400)

        if shares < heldshares:

            sale = -abs(sellstock["price"]*shares)

            # log sale in user portfolio
            db.execute("INSERT INTO portfolio (stock, symbol, price, shares, holdings, userID) VALUES (?, ?, ?, ?, ?, ?)",
                       sellstock["name"], sellstock["symbol"], float(sellstock["price"]), shares, sale, session["id"])

            # update user's cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", sale, session["id"])

            # redirect user to home page
            return redirect("/")

    else:
        return render_template("sell.html", portfolio=portfolio)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash"""
    # get amount of cash
    if request.method == "GET":
        return render_template("cash.html")

    else:
        addcash = request.form.get("addCash")
        if not addcash:  # validate cash amount input
            return apology("invalid amount", 400)
        addcash = float(addcash)

        # find user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["id"])[0]["cash"]

        if not cash:
            return apology("invalid command")

        else:
            cash = float(cash)

        # update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", addcash, session["id"])

        # redirect user to home page
        return redirect("/")
