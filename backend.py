from flask import Flask, redirec
t, jsonify
import sqlite3
import requests
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Workout Recommendation Logic
def recommend_workout(age, condition):
    if condition.lower() == "arthritis":
        return ["Swimming", "Yoga", "Low-impact cycling", "Pilates", "Resistance Band Exercises"]
    elif condition.lower() == "asthma":
        return ["Walking", "Swimming", "Cycling", "Yoga", "Low-intensity Strength Training"]
    elif condition.lower() == "nerve weakness":
        return ["Balance Exercises", "Tai Chi", "Light Resistance Training", "Stretching", "Pilates"]
    elif condition.lower() == "diabetes":
        return ["Brisk Walking", "Cycling", "Strength Training", "Stretching", "Rowing"]
    elif condition.lower() == "obesity":
        return ["Elliptical Machine", "Swimming", "Bodyweight Squats", "Dancing", "Water Aerobics"]
    else:
        return ["Strength Training", "Running", "HIIT", "Jump Rope", "Rowing Machine", "Boxing"]

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    age = int(request.args.get("age", 25))
    condition = request.args.get("condition", "None")
    workout_plan = recommend_workout(age, condition)
    
    return jsonify({"workout_plan": workout_plan, "message": "Personalized workout generated!"})

# Meal Tracking API
@app.route("/log_meal", methods=["POST"])
def log_meal():
    data = request.json
    user, food, calories, protein, carbs, fats = data["user"], data["food"], data["calories"], data["protein"], data["carbs"], data["fats"]
    
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals (user, food, calories, protein, carbs, fats) VALUES (?, ?, ?, ?, ?, ?)",
                   (user, food, calories, protein, carbs, fats))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Meal logged successfully!"})

@app.route("/get_meals", methods=["GET"])
def get_meals():
    user = request.args.get("user")
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals WHERE user=?", (user,))
    meals = cursor.fetchall()
    conn.close()
    
    return jsonify({"meals": meals})

# googlefit API Integration

app = Flask(__name__)

# 🔹 Google Fit API Credentials (Replace these with actual values)
GOOGLE_CLIENT_ID = "1062360637675-rkc55tlugvpv4pma7bt17blag2hrv22n.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_FIT_DATA_URL = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

# ✅ Step 1: Redirect users to Google OAuth for login
@app.route("/login")
def login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=https://www.googleapis.com/auth/fitness.activity.read "
        f"https://www.googleapis.com/auth/fitness.body.read"
    )
    return redirect(google_auth_url)

# ✅ Step 2: Handle OAuth callback & exchange code for access token
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(TOKEN_URL, data=token_data)
    
    if response.status_code == 200:
        tokens = response.json()
        return jsonify(tokens)  # Returns access_token and refresh_token
    else:
        return jsonify({"error": "Failed to authenticate"}), 400

# ✅ Step 3: Fetch Google Fit Steps, Calories & Weight Data
def fetch_google_fit_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    body = {
        "aggregateBy": [
            {"dataTypeName": "com.google.step_count.delta"},
            {"dataTypeName": "com.google.calories.expended"},
            {"dataTypeName": "com.google.weight"}  # Fetch weight data
        ],
        "bucketByTime": {"durationMillis": 86400000},  # 1 day
        "startTimeMillis": int((time.time() - 86400) * 1000),  # Yesterday
        "endTimeMillis": int(time.time() * 1000)  # Today
    }

    response = requests.post(GOOGLE_FIT_DATA_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch Google Fit data"}

@app.route("/get_google_fit_data", methods=["GET"])
def get_google_fit_data():
    access_token = request.headers.get("Authorization").split("Bearer ")[-1]
    return jsonify(fetch_google_fit_data(access_token))

if __name__ == "__main__":
    app.run(debug=True)

# Weight Tracking Feature
def log_weight(user_id, weight):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            date TEXT
        )
    """)
    cursor.execute("INSERT INTO weight_log (user_id, weight, date) VALUES (?, ?, ?)", (user_id, weight, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    return {"message": "Weight logged successfully"}

@app.route("/log_weight", methods=["POST"])
def log_weight_api():
    data = request.json
    user_id, weight = data["user_id"], data["weight"]
    return jsonify(log_weight(user_id, weight))

@app.route("/get_weight", methods=["GET"])
def get_weight():
    user_id = request.args.get("user_id")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, weight FROM weight_log WHERE user_id = ? ORDER BY date", (user_id,))
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        return jsonify({"message": "No weight data available."})
    
    return jsonify({"weight_data": data})

if __name__ == "__main__":
    # Initialize databases
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            food TEXT,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fats REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
    
    app.run(debug=True)
