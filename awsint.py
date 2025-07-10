from flask import Flask, flash, redirect, render_template, request, jsonify, session, url_for
import boto3
import uuid
from datetime import datetime

from flask_mail import Mail, Message

# Step 1: Create the Flask app instance
app = Flask(__name__)

# Step 2: Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace with your region

# Tables
photographers_table = dynamodb.Table('photographers')
bookings_table = dynamodb.Table('booking')

photographers = [
    {"id": "p1", "name": "amit", "skills": ["Wedding", "Portrait"], "image": "amit.jpg","location":"Hyderabad"},
    {"id": "p2", "name": "sana", "skills": ["Fashion", "Event"], "image": "sana.jpg","location":"Mumbai"},
    {"id": "p3", "name": "robo", "skills": ["All Events", "Event"], "image": "photo.jpg","location":"Benguluru"}
]

availability_data = {
    "p1": ["2025-06-20", "2025-06-23"],
    "p2": ["2025-06-19", "2025-06-22"],
    "p3": ["2025-07-21", "2025-07-26"]
}
 
 #Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login credentials here
        username = request.form['username']
        password = request.form['password']
        # Example check (replace with DB check)
        if username == 'admin' and password == '1234':
            session['user'] = username
            return redirect('/show-photographers')
        else:
            
            ('Invalid login credentials')
            return redirect('/login')
    return render_template('login.html')

#Signup
@app.route('/signup', methods=['POST'])
def signup():
    # Handle new user registration
    username = request.form['newUsername']
    password = request.form['newPassword']
    # Save user to database or file (not shown here)
    flash('Signup successful! You can now log in.')
    return redirect('/login')

#Logout
@app.route("/logout")
def logout():
    return render_template("logout.html")

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Booking form route
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        user_id = request.form.get('user_id')
        date = request.form.get('date')

        # Create unique booking ID
        booking_id = str(uuid.uuid4())

        # Store booking in DynamoDB Bookings table
        bookings_table.put_item(Item={
            'booking_id': booking_id,
            'photographer_id': photographer_id,
            'user_id': user_id,
            'date': date,
            'timestamp': datetime.now().isoformat()
        })

        return f"<h2 style='color:green;'>Booking Confirmed! For {photographer_id} on {date}.</h2><a href='/'>Back to Home</a>"

    return render_template('book.html')
#Portfolio
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", photographers=photographers, availability_data=availability_data)

#Contact
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Display photographers from DynamoDB
@app.route('/show-photographers')
def show_photographers():
    query = request.args.get('location', '').lower()
    if query:
        filtered = [p for p in photographers if query in p['location'].lower()]
    else:
        filtered = photographers

    return render_template(
        'photographers.html',
        photographers=filtered,
        availability_data=availability_data,
        request=request  # ✅ Pass request to template
    )

@app.route('/my-bookings')
def my_bookings():
    bookings = []  # Replace with actual user bookings from your database
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/search')
def search_photographers():
    category = request.args.get('category')
    location = request.args.get('location')

    # Filter photographers by category (skills) and location (case insensitive)
    results = [
        p for p in photographers
        if category in p['skills'] and location.lower() in p['location'].lower()
    ]

    return render_template('results.html', results=results, category=category, location=location)
#Payment
@app.route("/payment", methods=["GET", "POST"])
def payment():
    booking = session.get("booking_details")
    if not booking:
        return redirect(url_for("book"))

    if request.method == "POST":
        selected_package = request.form.get("package")
        return redirect(url_for("confirmation", package=selected_package))

    return render_template("payment.html", booking=booking)

@app.route("/confirmation", methods=["POST"])
def confirmation():
    package = request.args.get("package") or request.form.get("package")
    booking = session.get("booking_details")

    # Optional: Send confirmation email
    if booking:
        msg = Message(
            subject="📸 Booking Confirmed - Capture Moments",
            sender=app.config['MAIL_USERNAME'],
            recipients=[booking["email"]],
            body=f"""Hello {booking['full_name']},

Thank you for booking with Capture Moments!

✔ Photographer ID: {booking['photographer_id']}
📅 Date: {booking['date']}
📦 Package: {package}
📍 Location: {booking['location']}

We’ll follow up with details and confirmations. Feel free to reach out if you need anything.

— The Capture Moments Team
"""
        )
        Mail.send(msg)

    return render_template("confirmation.html", booking=booking, package=package)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

