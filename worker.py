from flask import Flask, request, jsonify
import os
import logging
import requests

app = Flask(__name__)

logging.basicConfig(filename='worker.log', level=logging.DEBUG if os.environ.get('DEBUG', 'False') == 'True' else logging.INFO)
logger = logging.getLogger()

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')
MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')

@app.route('/process_task', methods=['POST'])
def process_task():
    task = request.json
    logger.info(f"Received task: {task}")

    if task.get('target') == 'master':
        headers = {'Authorization': f'Bearer {MASTER_BEARER_TOKEN}'}
        response = requests.post(f"{MASTER_URL}/tasks/process", json=task, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error processing task on master: {response.text}")
            return jsonify({"error": "Failed to process task on master"}), 500
        
        result = response.json()
        return jsonify(result)
    else:
        result = {"status": "success", "result": "Task processed locally"}
        return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Worker shutting down...'

def create_worker_app():
    return app
