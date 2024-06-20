from flask import Blueprint, request, jsonify
import logging
import os

task_processing_bp = Blueprint('task_processing', __name__, url_prefix='/tasks')

logger = logging.getLogger()

@task_processing_bp.route('/process', methods=['POST'])
def process_task():
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.environ.get('MASTER_BEARER_TOKEN')}":
        return jsonify({"error": "Unauthorized"}), 401

    task = request.json
    logger.info(f"Received task: {task}")

    task_type = task.get('type')
    if task_type == 'example':
        result = {"status": "success", "result": "Task processed"}
    else:
        result = {"status": "error", "result": "Unknown task type"}

    return jsonify(result)