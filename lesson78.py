from crypt import methods
from socket import send_fds
from flask import Flask, redirect, url_for, render_template, request, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    def __init__(self, name, email):
        self.name = name
        self.emmail = email

class books(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.String(50))
    img = db.Column(db.String(50))
    
    def __init__(self, name, price, link_img):
        self.name = name
        self.price = price
        self.link_img = link_img

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        
        flash("Login successful")
        return redirect(url_for("user"))
    
    if "user" in session:
        flash("Already login")
        return redirect(url_for("user"))
    
    return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    flash("You are not logined in!")
    return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values=books.query.all())

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You are logged out, {user}")
        session.pop("user", None)
        session.pop("email", None)
        return redirect(url_for("login"))
    flash("You have not already logined in")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)