from flask import Blueprint, render_template, request, jsonify
import os
import subprocess

ssh_commands_bp = Blueprint('ssh_commands', __name__, url_prefix='/ssh_commands')

@ssh_commands_bp.route('/')
def index():
    return render_template('ssh_commands.html')

@ssh_commands_bp.route('/execute', methods=['POST'])
def execute():
    data = request.json
    if 'command' not in data:
        return jsonify({"status": "error", "error": "No command provided"}), 400
    
    command = data['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    log_action(f"Executed SSH command: {command}")

    return jsonify({"status": "success", "output": result.stdout, "error": result.stderr})

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")
