from flask import Blueprint, render_template, request, jsonify
import requests
import os

worker_health_bp = Blueprint('worker_health', __name__, url_prefix='/worker_health')

@worker_health_bp.route('/')
def index():
    worker_url = os.environ.get('WORKER_URL', 'http://localhost:5001')
    response = requests.get(f"{worker_url}/health")
    health_status = response.json()
    return render_template('worker_health.html', health_status=health_status)

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")