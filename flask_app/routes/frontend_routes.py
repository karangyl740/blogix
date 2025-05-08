from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import requests

frontend_bp = Blueprint("frontend_bp", __name__)
API_BASE = "http://127.0.0.1:8000/api"

@frontend_bp.route("/")
def index():
    headers = {}
    if 'access_token' in session:
        headers['Authorization'] = f"Bearer {session['access_token']}"
    blogs = requests.get(API_BASE + "blogs/", headers=headers).json()
    categories = requests.get(API_BASE + "categories/", headers=headers).json()
    comments = requests.get(API_BASE + "comments/", headers=headers).json()
    users = requests.get(API_BASE + "users/", headers=headers).json()
    return render_template("index.html", blogs=blogs, categories=categories, comments=comments, users=users)

@frontend_bp.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        response = requests.post(API_BASE + "token/", data=data)
        if response.status_code == 200:
            session['access_token'] = response.json()['access']
            flash("Logged in successfully!", "success")
            return redirect(url_for("frontend_bp.index"))
        else:
            flash("Login failed. Check your credentials.", "danger")
    return render_template("login.html")

@frontend_bp.route("/signup", methods=["GET", "POST"])
def signup_form():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        response = requests.post(API_BASE + "users/", json=data)
        if response.status_code in [200, 201]:
            flash("Account created! Please log in.", "success")
            return redirect(url_for("frontend_bp.login_form"))
        else:
            flash("Signup failed. Try a different username.", "danger")
    return render_template("signup.html")

@frontend_bp.route("/logout")
def logout_form():
    session.pop('access_token', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("frontend_bp.index"))
