from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Define the base URLs for the existing APIs
API1_BASE_URL = 'http://localhost:5000'
API2_BASE_URL = 'http://localhost:5001'

@app.route('/getAvailableFlights', methods=['GET'])
def get_available_flights():
    # Make a request to the /getAvailableFlights endpoint of API1
    api1_response = requests.get(f'{API1_BASE_URL}/getAvailableFlights')

    # Return the response from API1
    return jsonify(api1_response.json()), api1_response.status_code

@app.route('/getTotalAmount', methods=['GET'])
def get_total_amount():
    # Get the flight number and number of seats from query parameters
    flight_number = request.args.get('flight_number')
    num_seats = int(request.args.get('num_seats', 0))  # Default to 0 if not provided

    if not flight_number:
        return jsonify({'error': 'Flight number is required'}), 400

    if not  num_seats:
        return jsonify({'error': 'number of seats is required'}), 400
    # Make a request to the /getTotalAmount endpoint of API2
    api2_response = requests.get(f'{API2_BASE_URL}/getTotalAmount', params=request.args)

    if api2_response.status_code == 200:
        # Check if the flight number is correct in API2 and seats are available
        selected_flight = api2_response.json().get('selected_flight')
        if selected_flight and selected_flight['flightNumber'] == flight_number and num_seats <= selected_flight['availableSeats']:
            # Payment successful
            return jsonify({'message': 'Payment successful'}), 200
        else:
            return jsonify({'error': 'Incorrect flight number or insufficient seats for payment'}), 400
    else:
        return jsonify({'error': 'Failed to retrieve data from API2'}), api2_response.status_code

@app.route('/payment', methods=['POST'])
def process_payment():
    # Get the flight number and number of seats from the request body
    flight_number = request.json.get('flight_number')
    num_seats = request.json.get('num_seats', 0)  # Default to 0 if not provided

    if not flight_number:
        return jsonify({'error': 'Flight number is required for payment'}), 400

    # Make a request to the /getAvailableFlights endpoint of API1
    api1_response = requests.get(f'{API1_BASE_URL}/getAvailableFlights')

    if api1_response.status_code == 200:
        available_flights = api1_response.json()['flights']

        # Find the flight with the specified flight number in API1
       # Make a request to the /getTotalAmount endpoint of API2
api2_response = requests.get(f'{API2_BASE_URL}/getTotalAmount', params=request.args)

if api2_response.status_code == 200:
    # Check if the flight number is correct in API2 and seats are available
    selected_flight = api2_response.json().get('selected_flight')
    if selected_flight:
        if selected_flight['flightNumber'] == flight_number and num_seats <= selected_flight['availableSeats']:
            # Introduce a condition for simulating payment failure for some other process
            if some_other_condition:
                # Payment failed due to other reasons (customize as needed)
                return jsonify({'error': 'Payment failed by network issues'}), 400
            else:
                # Payment successful
                return jsonify({'message': 'Payment successful'}), 200
        else:
            # Payment failed due to incorrect flight number or insufficient seats
            return jsonify({'error': 'Incorrect flight number or insufficient seats for payment'}), 400
    else:
        # Payment failed because no flight data is available
        return jsonify({'error': 'No flight data available for the given parameters'}), 400
else:
    # Payment failed due to failure to retrieve data from API2
    return jsonify({'error': 'Failed to retrieve data from API2'}), api2_response.status_code


if __name__ == '__main__':
    app.run(port=5003)  
