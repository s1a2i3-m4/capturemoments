from flask import Flask, jsonify, request
#Step 1: Create the Flask app instance
app = Flask(__name__)
#Step 2: Dummy data for photographers (simulating database)
photographers = [
{"id": "p1", "name": "Amit Lensman", "skills": ["Wedding", "Portrait"]},
{"id": "p2", "name": "Sana Clickz", "skills": ["Fashion", "Event"]}
]
#Step 3: Dummy availability data mapped by photographer ID
availability_data = {
    "p1": ["2025-06-20", "2025-06-23"],
    "p2": ["2025-06-19", "2025-06-22"]
}
#Route 1: GET /photographers
# Returns list of all photographers
@app.route('/photographers', methods=['GET'])
def get_photographers():
    return jsonify (photographers)
#Route 2: GET /availability/<photographer_id>
# Returns available dates for the given photographer
@app.route('/availability/<photographer_id>', methods=['GET'])
def check_availability (photographer_id):
    return jsonify({
        "photographer_id": photographer_id,
        "available_dates": availability_data.get(photographer_id, [])
})
# -------------------------
# Route 3: POST /book
# Accepts a booking request and returns confirmation
@app.route('/book', methods=['POST'])
def book_photographer():
    booking = request.get_json()
    print("Received booking request:", booking)
    return jsonify({
    "message": "Booking confirmed!",
    "booking_details": booking
  }), 201

# Step 4: Start the Flask server
if __name__ == '_main_':
    app.run(debug=True)