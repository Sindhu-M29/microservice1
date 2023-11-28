from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Define the base URLs for the existing APIs from environment variables
API1_BASE_URL = os.environ.get('API1_BASE_URL')
API2_BASE_URL = os.environ.get('API2_BASE_URL')

# API1_BASE_URL = "http://127.0.0.1:5000"
# API2_BASE_URL = "http://127.0.0.1:5001"


@app.route('/getAvailableFlights', methods=['GET'])
def get_available_flights():
    api1_response = requests.get(f'{API1_BASE_URL}/getAvailableFlights')
    return jsonify(api1_response.json()), api1_response.status_code

@app.route('/getTotalAmount', methods=['GET'])
def get_total_amount():
    # Forward the request to API2 without additional logic
    api2_response = requests.get(f'{API2_BASE_URL}/getTotalAmount', params=request.args)
    return jsonify(api2_response.json()), api2_response.status_code

@app.route('/payment', methods=['POST'])
def process_payment():
    # Forward the payment request to API1 to get available flights details
    api1_response = requests.get(f'{API1_BASE_URL}/getAvailableFlights')
    available_flights = api1_response.json().get('flights', [])

    flight_number = request.json.get('flight_number')
    num_seats = request.json.get('num_seats', 0)

    if not flight_number or num_seats <= 0:
        return jsonify({'error': 'Invalid input parameters'}), 400

    # Find the selected flight in the available flights
    selected_flight = next(
        (flight for flight in available_flights if flight['flightNumber'] == flight_number),
        None
    )

    if selected_flight and num_seats <= selected_flight['availableSeats']:
        # Simulate a payment success message
        return jsonify({'message': 'Payment successful'}), 200
    else:
        return jsonify({'error': 'Incorrect flight number or insufficient seats for payment'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
