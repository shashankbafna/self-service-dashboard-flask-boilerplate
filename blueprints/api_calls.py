from flask import Blueprint, render_template, request, jsonify
import requests
import os

api_calls_bp = Blueprint('api_calls', __name__, url_prefix='/api_calls')

@api_calls_bp.route('/')
def index():
    return render_template('api_calls.html')

@api_calls_bp.route('/execute', methods=['POST'])
def execute():
    api_url = request.form['api_url']
    response = requests.get(api_url)
    log_action(f"Called API: {api_url}")
    return jsonify({"status": response.status_code, "output": response.json()})

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")