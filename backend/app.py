from flask import Flask, request, jsonify
import database

app = Flask(__name__)

@app.route('/customers', methods=['GET'])
def get_customers():
    """Retrieve all customers."""
    customers = database.get_customers()
    return jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    """Add a new customer."""
    data = request.json
    database.add_customer(data['name'], data['company'], data['email'], data['telephone'], data['notes'], data['follow_up_date'])
    return jsonify({"message": "Customer added successfully!"})

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer."""
    data = request.json
    database.update_customer(customer_id, data['name'], data['company'], data['email'], data['telephone'], data['notes'], data['follow_up_date'])
    return jsonify({"message": "Customer updated successfully!"})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer."""
    database.delete_customer(customer_id)
    return jsonify({"message": "Customer deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
