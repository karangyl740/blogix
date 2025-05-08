from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import requests
from config import Config
from extensions import db
from routes.blog_routes import blog_bp
from routes.auth_routes import auth_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)

    with app.app_context():
        from models.models import BlogPost
        db.create_all()

    app.register_blueprint(blog_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/")
    def index():
        headers = {}
        if 'access_token' in session:
            headers['Authorization'] = f"Bearer {session['access_token']}"
        try:
            blogs = requests.get("http://127.0.0.1:8000/api/blogs/", headers=headers).json()
            categories = requests.get("http://127.0.0.1:8000/api/categories/", headers=headers).json()
            comments = requests.get("http://127.0.0.1:8000/api/comments/", headers=headers).json()
            users = requests.get("http://127.0.0.1:8000/api/users/", headers=headers).json()
        except requests.RequestException as e:
            flash(f"Failed to fetch data: {str(e)}", "danger")
            blogs = categories = comments = users = []
        return render_template("index.html", blogs=blogs, categories=categories, comments=comments, users=users)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            data = {
                "username": request.form["username"],
                "password": request.form["password"]
            }
            try:
                response = requests.post("http://127.0.0.1:8000/api/token/", data=data)
                if response.status_code == 200:
                    session['access_token'] = response.json()['access']
                    flash("Logged in successfully!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Login failed. Check your credentials.", "danger")
            except requests.RequestException as e:
                flash(f"Login failed: {str(e)}", "danger")
        return render_template("login.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            if request.is_json:
                data = request.get_json()
            else:
                data = {
                    "username": request.form.get("username"),
                    "email": request.form.get("email"),
                    "password": request.form.get("password")
                }
            try:
                response = requests.post("http://127.0.0.1:8000/api/users/", json=data)
                if response.status_code in [200, 201]:
                    flash("Account created! Please log in.", "success")
                    return redirect(url_for("login"))
                else:
                    flash("Signup failed. Try a different username or email.", "danger")
            except requests.RequestException as e:
                flash(f"Signup failed: {str(e)}", "danger")
        return render_template("signup.html")

    @app.route("/logout")
    def logout():
        session.pop('access_token', None)
        flash("Logged out successfully.", "info")
        return redirect(url_for("index"))

    @app.route("/api/auth/login", methods=["POST"])
    def api_login():
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"message": "Missing username or password"}), 400
        try:
            response = requests.post("http://127.0.0.1:8000/api/token/", data=data)
            if response.status_code == 200:
                token = response.json()['access']
                session['access_token'] = token
                return jsonify({"message": "Login successful", "access_token": token}), 200
            return jsonify({"message": "Invalid credentials"}), 401
        except requests.RequestException as e:
            return jsonify({"message": f"Login failed: {str(e)}"}), 500

    @app.route("/api/auth/signup", methods=["POST"])
    def api_signup():
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"message": "Missing username, email, or password"}), 400
        try:
            response = requests.post("http://127.0.0.1:8000/api/users/", json=data)
            if response.status_code in [200, 201]:
                return jsonify({"message": "Signup successful"}), 201
            return jsonify({"message": "Signup failed: " + response.json().get('message', 'Unknown error')}), 400
        except requests.RequestException as e:
            return jsonify({"message": f"Signup failed: {str(e)}"}), 500

    @app.route("/api/auth/logout", methods=["POST"])
    def api_logout():
        session.pop("access_token", None)
        return jsonify({"message": "Logged out"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)