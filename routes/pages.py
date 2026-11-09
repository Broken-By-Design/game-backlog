from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from routes import auth, items

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def home():
    return render_template("index.html", items=items.list_items())


@pages_bp.post("/items")
def add_item():
    body, status = items.add_item()
    if status != 201:
        flash(body["error"])
    return redirect(url_for("pages.home"))


@pages_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("pages.home"))
    if request.method == "POST":
        body, status = auth.register()
        if status == 201:
            flash("Account Created, You can log in now")
            return redirect(url_for("pages.login"))
        flash(body["error"])
    return render_template("register.html")


@pages_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("pages.home"))
    if request.method == "POST":
        auth.login()
        if "user_id" in session:
            return redirect(url_for("pages.home"))
        flash("Invalid username or password")
    return render_template("login.html")


@pages_bp.post("/logout")
def logout():
    auth.logout()
    return redirect(url_for("pages.home"))
