from flask import Blueprint, request, jsonify, session
import requests

auth_bp = Blueprint("auth", __name__)
API_BASE = "http://127.0.0.1:8000/api"

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing username or password"}), 400
    try:
        response = requests.post(f"{API_BASE}/token/", data=data)
        if response.status_code == 200:
            token = response.json()['access']
            session['access_token'] = token
            return jsonify({"message": "Login successful", "access_token": token}), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except requests.RequestException as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing username, email, or password"}), 400
    try:
        response = requests.post(f"{API_BASE}/users/", json=data)
        if response.status_code in [200, 201]:
            return jsonify({"message": "Signup successful"}), 201
        return jsonify({"message": "Signup failed: " + response.json().get('message', 'Unknown error')}), 400
    except requests.RequestException as e:
        return jsonify({"message": f"Signup failed: {str(e)}"}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("access_token", None)
    return jsonify({"message": "Logged out"}), 200