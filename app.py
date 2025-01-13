from flask import Flask, render_template, jsonify, request, send_from_directory, Response, redirect
import requests
import bcrypt
import json


# We might not need to use all these imports now, but they'll definitely come in useful in future.

app = Flask(__name__)

def load_accounts():
	with open('accounts.json', 'r') as f:
		j = json.load(f)
		return j

def write_accounts(accounts):
	with open('accounts.json', 'w') as f:
		json.dump(accounts, f)
	return "OK"

def js_create_account(username, password):
	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
	accounts = load_accounts()
	if username in accounts:
		return jsonify({'message': 'Username already exists'})
	accounts[username] = {}
	accounts[username]['password_hashed'] = hashed.decode('utf-8')
	write_accounts(accounts)
	return jsonify({'message': 'Account created successfully'})

def check_login(username, password):
	accounts = load_accounts()
	if not username in accounts:
		return jsonify({'message': 'Account not found'})
	if bcrypt.checkpw(password.encode('utf-8'), accounts[username]['password_hashed'].encode('utf-8')):
		return jsonify({'message': 'Login successful'})
	else:
		return jsonify({'message': 'Invalid password'})

@app.route('/')
def index():
	return redirect('/login') # We can add an actual homepage later

@app.route('/dashboard')
def dashboard():
	return redirect('/in_progress') # We'll work on this once the login system's running smoothly.

@app.route('/reset_password')
def reset_password():
	return redirect('/in_progress')

@app.route('/in_progress')
def in_progress():
	return "<h1>Site in Progress</h1><p>This part of the site is still under construction. Check back soon!</p>"

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/api/create_account', methods=['GET', 'POST'])
def create_account():
	j = request.get_json()
	username = j['username']
	password = j['password']
	return js_create_account(username, password)

@app.route('/api/login', methods=['GET', 'POST'])
def verify_login():
	j = request.get_json()
	username = j['username']
	password = j['password']
	return check_login(username, password)

if __name__ == '__main__':
	app.run(debug=True, port='1234', host='0.0.0.0')
