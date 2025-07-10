from flask import Flask, flash, redirect, render_template, request, jsonify, url_for, session
from flask_mail import Mail, Message

# Step 1: Create the Flask app instance
app = Flask(__name__)
app.secret_key = "something_secure_and_unique"  # Required for session

# Step 2: Configure Flask-Mail after creating the app
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'saimanikantabamini@gmail.com'       # Replace with your email
app.config['MAIL_PASSWORD'] = 'merf zylk wkxf mlrd'            # Replace with app password

mail = Mail(app)

# Step 3: Dummy data for photographers (simulating database)
photographers = [
    {"id": "p1", "name": "amit", "skills": ["Wedding", "Portrait"], "image": "amit.jpg","location":"Hyderabad"},
    {"id": "p2", "name": "sana", "skills": ["Fashion", "Event"], "image": "sana.jpg","location":"Mumbai"},
    {"id": "p3", "name": "robo", "skills": ["All Events", "Event"], "image": "photo.jpg","location":"Benguluru"}
]

availability_data = {
    "p1": ["2025-06-20", "2025-06-23"],
    "p2": ["2025-06-19", "2025-06-22"]
}

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        user_id = request.form.get('user_id')
        date = request.form.get('booking_date')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        location = request.form.get('location')
        notes = request.form.get('notes')

        session['booking_details'] = {
            "photographer_id": photographer_id,
            "user_id": user_id,
            "date": date,
            "full_name": full_name,
            "email": email,
            "contact": contact,
            "location": location,
            "notes": notes
        }

        return redirect(url_for("payment"))
    return render_template('book.html')

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
            flash('Invalid login credentials')
            return redirect('/login')
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    # Handle new user registration
    username = request.form['newUsername']
    password = request.form['newPassword']
    # Save user to database or file (not shown here)
    flash('Signup successful! You can now log in.')
    return redirect('/login')


@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", photographers=photographers, availability_data=availability_data)

@app.route('/my-bookings')
def my_bookings():
    bookings = []  # Replace with actual user bookings from your database
    return render_template('my_bookings.html', bookings=bookings)



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
        mail.send(msg)

    return render_template("confirmation.html", booking=booking, package=package)

if __name__ == '_main_':
    app.run(debug=True)