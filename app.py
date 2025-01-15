from flask import Flask, render_template, jsonify, request, send_from_directory, Response, redirect
import requests
import bcrypt
import json
import random


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
	ids = []
	for account in accounts:
		ids.append(accounts[account]['id'])
	accounts[username]['id'] = generate_user_id(ids)
	write_accounts(accounts)
	return jsonify({'message': 'Account created successfully'})

def get_username(id):
	accounts = load_accounts()
	for account in accounts:
		if accounts[account]['id'] == id:
			return accounts[account]['username']
	return None

def get_id(username):
	accounts = load_accounts()
	for account in accounts:
		if accounts[account]['username'] == username:
			return accounts[account]['id']
	return None

def check_login(username, password):
	accounts = load_accounts()
	if not username in accounts:
		return jsonify({'message': 'Account not found'})
	if bcrypt.checkpw(password.encode('utf-8'), accounts[username]['password_hashed'].encode('utf-8')):
		return jsonify({'message': 'Login successful'})
	else:
		return jsonify({'message': 'Invalid password'})

def authenticate(username, password):
	accounts = load_accounts()
	if not username in accounts:
		return False
	if bcrypt.checkpw(password.encode('utf-8'), accounts[username]['password_hashed'].encode('utf-8')):
		return True
	else:
		return False

def get_chat(chat_id):
	try:
		with open(f"chats/{chat_id}.json", 'r') as f:
			return json.load(f)
	except:
		return None

def write_chat(chat_id, data):
	with open(f"chats/{chat_id}.json", 'w') as f:
		json.dump(chat, f)

def get_participants(chat):
	participants = []
	for participant in chat["participants"]:
		participants.append(chat["participants"][participant]["id"])
	return participants

def generate_id(messages):
	ids = []
	for message in messages:
		ids.append(message['id'])
	id = ''.join(str(random.randint(0,9)) for _ in range(8))
	while id in ids:
		id = ''.join(str(random.randint(0,9)) for _ in range(8))
	return id

def generate_user_id(ids):
	id = ''.join(str(random.randint(0,9)) for _ in range(12))
	while id in ids:
		id = ''.join(str(random.randint(0,9)) for _ in range(12))
	return id
	

def send_message(chat_id, author_id, content):
	chat = get_chat(chat_id)
	if chat == None:
		return jsonify({"id":None})
	if not author_id in get_participants(chat):
		return jsonify({"id":None})
	messages = chat["messages"]
	id = generate_id(messages)
	messages.append({
		"id":id,
		"author":author_id,
		"content":content
	})
	chat["messages"] = messages
	write_chat(chat_id, chat)
	return jsonify({"id":id})

def is_allowed(username, password, chat_id):
	return authenticate(username, password) and get_id(username) in get_participants(get_chat(chat_id))

def get_user_data(id):
	accounts = load_accounts()
	for account in accounts:
		if accounts[account]['id'] == id:
			them = accounts[account]
			del them["password_hashed"]
			return jsonify(them)
	return jsonify({"error":"user not found"}), 404

@app.route('/api/chats/<id>', methods=['POST'])
def api_chat_id(id):
	b = request.get_json(force=True)
	if is_allowed(b['username'], b['password'], id):
		return get_chat(id)
	else:
		return jsonify({"error":"unauthenticated"}), 401

@app.route('/api/chats/<id>/post_message', methods=['POST'])
def post_message_api(id):
	b = request.get_json(force=True)
	if is_allowed(b['username'], b['password'], id):
		return send_message(id, get_id(b['username']), b['content'])
	else:
		return jsonify({"error":"unauthenticated"}), 401

@app.route('/api/users/<id>')
def api_users(id):
	return get_user_data(id)
	

@app.route('/')
def index():
	return redirect('/login') # We can add an actual homepage later

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

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
