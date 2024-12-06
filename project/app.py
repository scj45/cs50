from cs50 import SQL
import requests
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

DEBUG = True

# Configure application
app = Flask(__name__, static_folder='staticfiles')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///library.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear() # Forget any user_id

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM reader WHERE username = ?", request.form.get("username"))

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

        if not username or not password or not confirmation:
            return apology("missing field", 400)

        taken = db.execute("SELECT * FROM reader WHERE username = ?", username)

        if len(taken) >= 1:
            return apology("username already taken", 400)
        else:
            hash = generate_password_hash(password)
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            phone = request.form.get("phone")
            result = db.execute("INSERT INTO reader (username, firstname, lastname, hash, email, phoneno) VALUES(?, ?, ?, ?, ?, ?)", username, firstname, lastname, hash, email, phone)
            session["id"] = result
            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/")
@login_required
def index():
    """Homepage"""
    #get the latest books
    latest = db.execute("SELECT books.title, authorfirstname, authorlastname, year, edition FROM books INNER JOIN history ON books.id = history.bookid WHERE readerid = ? ORDER BY timestamp DESC LIMIT 5", session["id"])
    return render_template("index.html", latest=latest)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
     """Search using a keyword"""
     if request.method == "POST":
        print("Form submitted")
        keyword = request.form.get("keyword")
        print(f"Keyword received: {keyword}")
        results = db.execute("SELECT * FROM books WHERE title LIKE ? OR authorfirstname LIKE ? OR authorlastname LIKE ? OR year LIKE ? OR genre LIKE ? OR topicsA LIKE ? OR topicsB LIKE ? OR topicsC LIKE ?", keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword)
        # display search results
        return render_template("results.html", keyword=keyword, results=results)

     else:
        return render_template("search.html")

@app.route("/browse", methods=["GET", "POST"])
@login_required
def browse():
    """Browse the collection"""
    books = db.execute("SELECT * FROM books ORDER BY authorlastname")
    return render_template("browse.html", books=books)


@app.route("/log", methods=["GET", "POST"]) #to do
@login_required
def log():
    """Log a new book into library"""
    if request.method == "POST":
        title = request.form.get("title")
        authorfirst = request.form.get("authorfirst")
        authorlast = request.form.get("authorlast")
        year = request.form.get("year")
        edition = request.form.get("edition")
        copies = request.form.get("copies")
        genre = request.form.get("checkedValues")
        topicsA = request.form.get("topicsA")
        topicsB = request.form.get("topicsB")
        topicsC = request.form.get("topicsC")

        exist = db.execute("SELECT * from books where title = ? AND authorfirstname = ? AND authorlastname = ? AND year = ? AND edition = ?", title, authorfirst, authorlast, year, edition)

        if len(exist) >=1:
            return apology("Book already logged", 400)
        else:
            db.execute("INSERT INTO books (title, authorfirstname, authorlastname, year, edition, copies, genre, topicsA, topicsB, topicsC) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", title, authorfirst, authorlast, year, edition, copies, genre, topicsA, topicsB, topicsC)
            bookid = db.execute("SELECT last_insert_rowid()")[0]['last_insert_rowid()']
            action = str("logged")
            db.execute("INSERT INTO history (bookid, title, readerid, action) VALUES (?, ?, ?, ?)", bookid, title, session["id"], action)
            return redirect ("/")
    else:
        return render_template("log.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Display session history of logged in user"""
    history = db.execute("SELECT bookID, title, action, timestamp FROM history WHERE readerID = ?", session["id"])
    print(history)

    return render_template("history.html", history=history)

@app.route("/finish", methods=["GET", "POST"])
@login_required
def finish():
    if request.method == "POST":
        title = request.form.get("title")
        authorfirstname = str(request.form.get("authorfirst"))
        authorlastname = str(request.form.get("authorlast"))
        rating = request.form.get("rating")
        action = str("read")

        bookid = db.execute("SELECT id FROM books WHERE title=? AND authorlastname=?", title, authorlastname)
        if bookid:
            bookid = bookid[0]["id"]
        else:
            # Handle the case where no book is found
            return "Book not found", 404

        db.execute("INSERT INTO finished (bookid, title, authorfirstname, authorlastname, readerid, rating) VALUES (?, ?, ?, ?, ?, ?)", bookid, title, authorfirstname, authorlastname, session["id"], rating)
        db.execute("INSERT INTO history (bookid, title, readerid, action) VALUES (?, ?, ?, ?)", bookid, title, session["id"], action)
        return redirect("/")

    else:
        return render_template("finish.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
