from flask import Blueprint, render_template, request, flash
import os

user_actions_bp = Blueprint('user_actions', __name__, url_prefix='/user_actions')

@user_actions_bp.route('/history')
def history():
    actions = []
    if os.path.exists('user_actions.log'):
        with open('user_actions.log', 'r') as file:
            actions = file.readlines()
    return render_template('user_actions.html', actions=actions)

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")

def send_task_to_master(task):
    headers = {'Authorization': f'Bearer {os.environ.get('MASTER_BEARER_TOKEN')}'}
    response = requests.post(f"{os.environ.get('MASTER_URL')}/tasks/process", json=task, headers=headers)
    if response.status_code == 200:
        log_action(f"Task sent to master: {task}")
    else:
        log_action(f"Failed to send task to master: {task}")