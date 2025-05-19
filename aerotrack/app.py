from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"  # Secret key for session management

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # replace with your MySQL password
    database="flight_booking"
)
cursor = conn.cursor(dictionary=True)

# Home route (Login page)
@app.route("/")
def home():
    return render_template("login.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])  # Hash the password for security
        # Insert user details into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        return redirect("/")  # Redirect to login after signup
    return render_template("signup.html")

# Login route
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    # Fetch user from database
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    # Validate credentials
    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]  # Set session
        return redirect("/dashboard")
    return "Invalid credentials"

# Dashboard route
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")  # Redirect if not logged in
    return render_template("dashboard.html")

# Search Flights route
@app.route("/flights", methods=["GET", "POST"])
def search_flights():
    flights = None
    journey_date = None
    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]
        journey_date = request.form["journey_date"]
        # Query for available flights
        cursor.execute("""
            SELECT * FROM flights
            WHERE source = %s AND destination = %s AND DATE(departure) = %s
        """, (source, destination, journey_date))
        flights = cursor.fetchall()
    return render_template("search_flight.html", flights=flights, journey_date=journey_date)

# Book Flight route
@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
def book_flight(flight_id):
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        seat = request.form["seat"]
        meal = request.form["meal"]
        user_id = session["user_id"]

        # Store booking details
        cursor.execute("""
            INSERT INTO bookings (user_id, flight_id, seat_number, meal_preference, passenger_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, flight_id, seat, meal, name))
        conn.commit()

        booking_id = cursor.lastrowid
        return redirect(f"/payment/{booking_id}")

    return render_template("book_flight.html", flight_id=flight_id)

# Payment route
@app.route("/payment/<int:booking_id>", methods=["GET", "POST"])
def payment(booking_id):
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        method = request.form["method"]
        upi_id = request.form.get("upi_id")
        card_name = request.form.get("card_name")
        card_number = request.form.get("card_number")
        expiry = request.form.get("expiry")
        cvv = request.form.get("cvv")

        # Store payment details
        cursor.execute("""
            INSERT INTO payments (
                booking_id, method, upi_id, card_name, card_number, expiry, cvv
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (booking_id, method, upi_id, card_name, card_number, expiry, cvv))
        conn.commit()

        return render_template("booking_success.html")

    return render_template("payment.html", booking_id=booking_id)

# User Profile route
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    if request.method == "POST":
        name = request.form["name"]
        passport = request.form["passport"]
        contact = request.form["contact"]
        # Save profile information
        cursor.execute("""
            INSERT INTO passengers (user_id, full_name, passport_number, contact_info)
            VALUES (%s, %s, %s, %s)
        """, (user_id, name, passport, contact))
        conn.commit()
    # Retrieve profile details
    cursor.execute("SELECT * FROM passengers WHERE user_id = %s", (user_id,))
    profile = cursor.fetchone()
    return render_template("profile.html", profile=profile)

# Feedback route
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "user_id" not in session:
        return redirect("/")
    if request.method == "POST":
        message = request.form["message"]
        # Store feedback
        cursor.execute("INSERT INTO feedback (user_id, message) VALUES (%s, %s)",
                       (session["user_id"], message))
        conn.commit()
        return "Feedback submitted successfully!"
    return render_template("feedback.html")

# Support route
@app.route("/support")
def support():
    return render_template("support.html")

# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask application
