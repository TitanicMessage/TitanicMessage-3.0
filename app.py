from flask import Flask, render_template, jsonify, request, send_from_directory, Response
import requests
import bcrypt
import json

# We might not need to use all these imports now, but they'll definitely come in useful in future.

app = Flask(__name__)
app.url_map.strict_slashes = False # Making sure 'site/page' is equal to 'site/page/'

if __name__ == '__main__':
	app.run(debug=True, port='8080', host='0.0.0.0')
