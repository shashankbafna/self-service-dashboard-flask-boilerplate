from flask import Flask, render_template, redirect, url_for, flash
from config import DevelopmentConfig, ProductionConfig
import os
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig if app.config['DEBUG'] else ProductionConfig)

    # Configure logging
    logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.DEBUG if app.config['DEBUG'] else logging.INFO)
    logger = logging.getLogger()

    # Register blueprints
    from blueprints.user_actions import user_actions_bp
    from blueprints.file_management import file_management_bp
    from blueprints.worker_health import worker_health_bp
    from blueprints.ssh_commands import ssh_commands_bp
    from blueprints.api_calls import api_calls_bp
    from blueprints.task_processing import task_processing_bp

    app.register_blueprint(user_actions_bp)
    app.register_blueprint(file_management_bp)
    app.register_blueprint(worker_health_bp)
    app.register_blueprint(ssh_commands_bp)
    app.register_blueprint(api_calls_bp)
    app.register_blueprint(task_processing_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app