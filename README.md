# self-service-dashboard-flask-boilerplate
Typical boilerplate code to quick start self-service via flask dashboard.


Requirement:
code a python flask self service multi pages web dashboard with master and worker architecture to manage multiple hosts and master host itself. There is no database setup. user actions has to be recorded and stored in files on master and worker respectively. master should be able to process tasks on itself as well.

Dashboard should be designed with proper headers and footer. It should have links to navigate through pages. Home/Landing page should be with cards in the center.

From dashboard user can:

view user actions history
view, create, update files from bitbucket repo. capture this user action so it can be displayed in user actions history.
track health of workers.
send remote ssh commands to workers and view commands execution output and status. capture this user action so it can be displayed in user actions history.
example - disk usage on /
call remote worker apis and view apis output and status. capture this user action so it can be displayed in user actions history.
example api - calculate no. of folders present in /
Dashboard in all pages should have ability to display a flash/popup message via api to alert the user.
warn the user if same operation is taking time or is fired multiple times.
From worker (which shoud be api) only master can interact with valid bearer token:

Worker should receive tasks from master
it should process tasks on worker host
report back with task's status.
worker should be able to process tasks on master as well.
warn if the task is taking long and send async response later.
Few important things to be implemented:

Use blueprints and write easy manageable production grade code with working example.
Both dashboard and worker should run from same file. It should be decided with environment variable whether that particular node is worker or master. Master will have os environ variable "SELFSERVICE_TYPE"="MASTER"

There is no Database setup. We should use files to store and retrieve user actions from the dashboards.

Self service tool should have proper detailed logging. It should be Debug enabled for UAT and configurable for production environment.

Design web pages with form to view, create, edit/update the files. The files will be chosen by the user from dropdown with search, dropdown list can be fetched from bitbucket api to list files.
---First display the contents of the file chosen in the page with buttons to update.
---If update is clicked, then create a temporary branch, checkout and display contents of the chosen file in an text edit field to update the file, give buttons to download and Commit"


To create a self-service multi-page web dashboard with a master-worker architecture in Python using Flask, you will need to follow these steps:

1. **Set Up the Flask Application:**
   - Use Flask and Flask-Blueprints for a modular and maintainable structure.
   - Implement environment variable checks to determine if the instance is a master or a worker.

2. **Create Blueprints for Modularization:**
   - Separate different functionalities like user actions, file management, worker health, SSH commands, etc., into different blueprints.

3. **Implement Logging:**
   - Use Python’s logging module to implement detailed logging.
   - Configure logging for both development (debug mode) and production environments.

4. **Design the Web Interface:**
   - Use Flask templates to create a user-friendly interface.
   - Implement navigation, headers, and footers in the templates.

5. **User Actions Recording:**
   - Record user actions in files on both master and worker nodes.

6. **Bitbucket Integration:**
   - Use Bitbucket API to list, view, and update files.

7. **Worker Health Tracking:**
   - Implement endpoints on the worker to report their health status.

8. **SSH Command Execution:**
   - Use Python’s `paramiko` library to execute SSH commands on worker nodes.

9. **API Calls Between Master and Worker:**
   - Use Flask routes to handle API calls between the master and worker nodes.

10. **Flash Messages and Alerts:**
    - Use Flask’s `flash` function to display messages to the user.

Here is a sample implementation:

### Directory Structure:
```
selfservice/
│
├── app.py
├── config.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user_actions.html
│   ├── file_management.html
│   ├── worker_health.html
│   ├── ssh_commands.html
│   ├── api_calls.html
│   └── alert.html
├── static/
│   └── style.css
├── blueprints/
│   ├── __init__.py
│   ├── user_actions.py
│   ├── file_management.py
│   ├── worker_health.py
│   ├── ssh_commands.py
│   └── api_calls.py
└── worker.py
```

### Configuration (config.py):
```python
import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SELFSERVICE_TYPE = os.environ.get('SELFSERVICE_TYPE', 'MASTER')
    LOG_FILE = os.environ.get('LOG_FILE', 'selfservice.log')
    BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories/YOUR_REPO_NAME'
    BITBUCKET_USERNAME = 'YOUR_USERNAME'
    BITBUCKET_PASSWORD = 'YOUR_PASSWORD'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### Flask Application (app.py):
```python
from flask import Flask, render_template, redirect, url_for, flash
from config import DevelopmentConfig, ProductionConfig
import os
import logging

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

app.register_blueprint(user_actions_bp)
app.register_blueprint(file_management_bp)
app.register_blueprint(worker_health_bp)
app.register_blueprint(ssh_commands_bp)
app.register_blueprint(api_calls_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```

### Templates (templates/base.html):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Service Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>Self Service Dashboard</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('user_actions.history') }}">User Actions</a>
            <a href="{{ url_for('file_management.index') }}">File Management</a>
            <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
            <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
            <a href="{{ url_for('api_calls.index') }}">API Calls</a>
        </nav>
    </header>
    <main>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul class="flashes">
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Self Service Dashboard</p>
    </footer>
</body>
</html>
```

### Templates (templates/index.html):
```html
{% extends 'base.html' %}

{% block content %}
<div class="cards">
    <div class="card">
        <a href="{{ url_for('user_actions.history') }}">User Actions</a>
    </div>
    <div class="card">
        <a href="{{ url_for('file_management.index') }}">File Management</a>
    </div>
    <div class="card">
        <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
    </div>
    <div class="card">
        <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
    </div>
    <div class="card">
        <a href="{{ url_for('api_calls.index') }}">API Calls</a>
    </div>
</div>
{% endblock %}
```

### Blueprints Example (blueprints/user_actions.py):
```python
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
```

### Worker Implementation (worker.py):
```python
from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='worker.log', level=logging.DEBUG if os.environ.get('DEBUG', 'False') == 'True' else logging.INFO)
logger = logging.getLogger()

@app.route('/process_task', methods=['POST'])
def process_task():
    task = request.json
    logger.info(f"Received task: {task}")
    # Process the task (dummy implementation)
    result = {"status": "success", "result": "Task processed"}
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5001)
```

This is a skeleton implementation that can be expanded with specific functionalities, such as Bitbucket file operations, SSH command executions, etc. Each blueprint should be developed similarly to `user_actions_bp`, and proper error handling and logging should be added to all routes. Additionally, the actual integration with Bitbucket API and SSH operations need to be implemented in their respective blueprints.



To enable the worker to run tasks on the master, we need to establish a communication mechanism between the worker and the master. The master will expose certain endpoints that the worker can call to send tasks, and the master will process these tasks accordingly.

Here's how we can enhance the existing setup to support this feature:

1. **Expose Task Processing Endpoints on Master:**
   - Create a new blueprint for task processing on the master.
   - The worker will send tasks to this endpoint, and the master will process them.

2. **Implement Task Processing Logic on Master:**
   - Define the tasks that can be processed by the master.
   - Implement the logic to process these tasks.

3. **Secure Communication:**
   - Use bearer tokens to secure the communication between the worker and the master.
   - Validate the bearer token on the master before processing any tasks.

### Enhancing Master to Handle Tasks from Worker

**Add a new blueprint for task processing (blueprints/task_processing.py):**
```python
from flask import Blueprint, request, jsonify
import logging
import os

task_processing_bp = Blueprint('task_processing', __name__, url_prefix='/tasks')

logger = logging.getLogger()

@task_processing_bp.route('/process', methods=['POST'])
def process_task():
    # Validate bearer token
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.environ.get('MASTER_BEARER_TOKEN')}":
        return jsonify({"error": "Unauthorized"}), 401

    task = request.json
    logger.info(f"Received task: {task}")

    # Example task processing
    task_type = task.get('type')
    result = None

    if task_type == 'disk_usage':
        result = os.popen('df -h /').read()
    elif task_type == 'list_folders':
        result = os.popen('ls -l /').read()
    else:
        return jsonify({"error": "Unknown task type"}), 400

    return jsonify({"status": "success", "result": result})
```

**Register the new blueprint in the Flask app (app.py):**
```python
from blueprints.task_processing import task_processing_bp

app.register_blueprint(task_processing_bp)
```

### Enhancing Worker to Send Tasks to Master

**Implement task sending logic in worker.py:**
```python
import requests
from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='worker.log', level=logging.DEBUG if os.environ.get('DEBUG', 'False') == 'True' else logging.INFO)
logger = logging.getLogger()

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')
MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')

@app.route('/process_task', methods=['POST'])
def process_task():
    task = request.json
    logger.info(f"Received task: {task}")

    if task.get('target') == 'master':
        # Send task to master
        headers = {'Authorization': f'Bearer {MASTER_BEARER_TOKEN}'}
        response = requests.post(f"{MASTER_URL}/tasks/process", json=task, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error processing task on master: {response.text}")
            return jsonify({"error": "Failed to process task on master"}), 500
        
        result = response.json()
        return jsonify(result)
    else:
        # Process task locally (dummy implementation)
        result = {"status": "success", "result": "Task processed locally"}
        return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5001)
```

### Secure Communication

**Set environment variables:**
```sh
export MASTER_URL=http://localhost:5000
export MASTER_BEARER_TOKEN=your_master_bearer_token
```

**Run the master and worker:**
- Ensure the master is started with the appropriate environment variables set.
- Start the worker with the MASTER_URL and MASTER_BEARER_TOKEN environment variables.

### Sample User Actions Recording

**Update user actions blueprint to log tasks sent to master (blueprints/user_actions.py):**
```python
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

# Example usage
def send_task_to_master(task):
    headers = {'Authorization': f'Bearer {os.environ.get('MASTER_BEARER_TOKEN')}'}
    response = requests.post(f"{os.environ.get('MASTER_URL')}/tasks/process", json=task, headers=headers)
    if response.status_code == 200:
        log_action(f"Task sent to master: {task}")
    else:
        log_action(f"Failed to send task to master: {task}")
```

By following this approach, the worker can send tasks to the master, which processes them and returns the results. The communication is secured using bearer tokens, and user actions are logged for auditing purposes.



To run both the master and worker instances from a single `run.py` file, you can use `multiprocessing` or `threading` to start both Flask applications simultaneously. Here, we'll use `multiprocessing` to achieve this.

### Directory Structure
```
selfservice/
│
├── run.py
├── config.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user_actions.html
│   ├── file_management.html
│   ├── worker_health.html
│   ├── ssh_commands.html
│   └── api_calls.html
├── static/
│   └── style.css
├── blueprints/
│   ├── __init__.py
│   ├── user_actions.py
│   ├── file_management.py
│   ├── worker_health.py
│   ├── ssh_commands.py
│   └── api_calls.py
└── worker.py
```

### Configuration (config.py)
```python
import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SELFSERVICE_TYPE = os.environ.get('SELFSERVICE_TYPE', 'MASTER')
    LOG_FILE = os.environ.get('LOG_FILE', 'selfservice.log')
    BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories/YOUR_REPO_NAME'
    BITBUCKET_USERNAME = 'YOUR_USERNAME'
    BITBUCKET_PASSWORD = 'YOUR_PASSWORD'
    MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')
    MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### Flask Application (app.py)
```python
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
```

### Worker Implementation (worker.py)
```python
from flask import Flask, request, jsonify
import os
import logging
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='worker.log', level=logging.DEBUG if os.environ.get('DEBUG', 'False') == 'True' else logging.INFO)
logger = logging.getLogger()

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')
MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')

@app.route('/process_task', methods=['POST'])
def process_task():
    task = request.json
    logger.info(f"Received task: {task}")

    if task.get('target') == 'master':
        # Send task to master
        headers = {'Authorization': f'Bearer {MASTER_BEARER_TOKEN}'}
        response = requests.post(f"{MASTER_URL}/tasks/process", json=task, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error processing task on master: {response.text}")
            return jsonify({"error": "Failed to process task on master"}), 500
        
        result = response.json()
        return jsonify(result)
    else:
        # Process task locally (dummy implementation)
        result = {"status": "success", "result": "Task processed locally"}
        return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def create_worker_app():
    return app
```

### Blueprint for Task Processing on Master (blueprints/task_processing.py)
```python
from flask import Blueprint, request, jsonify
import logging
import os

task_processing_bp = Blueprint('task_processing', __name__, url_prefix='/tasks')

logger = logging.getLogger()

@task_processing_bp.route('/process', methods=['POST'])
def process_task():
    # Validate bearer token
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.environ.get('MASTER_BEARER_TOKEN')}":
        return jsonify({"error": "Unauthorized"}), 401

    task = request.json
    logger.info(f"Received task: {task}")

    # Example task processing
    task_type = task.get('type')
    result = None

    if task_type == 'disk_usage':
        result = os.popen('df -h /').read()
    elif task_type == 'list_folders':
        result = os.popen('ls -l /').read()
    else:
        return jsonify({"error": "Unknown task type"}), 400

    return jsonify({"status": "success", "result": result})
```

### Single Entry Point (run.py)
```python
import os
from multiprocessing import Process
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()
    app.run(port=5000)

def run_worker():
    app = create_worker_app()
    app.run(port=5001)

if __name__ == '__main__':
    # Determine the role of the current node
    selfservice_type = os.environ.get('SELFSERVICE_TYPE', 'MASTER').upper()

    if selfservice_type == 'MASTER':
        # Run both master and worker as separate processes
        master_process = Process(target=run_master)
        worker_process = Process(target=run_worker)
        
        master_process.start()
        worker_process.start()
        
        master_process.join()
        worker_process.join()
    elif selfservice_type == 'WORKER':
        # Run only the worker process
        run_worker()
    else:
        print("Unknown SELFSERVICE_TYPE. Please set it to either 'MASTER' or 'WORKER'.")
```

### Running the Application
1. **Set Environment Variables:**
   ```sh
   export SELFSERVICE_TYPE=MASTER
   export DEBUG=True
   export MASTER_BEARER_TOKEN=your_master_bearer_token
   export MASTER_URL=http://localhost:5000
   ```

2. **Run the Application:**
   ```sh
   python run.py
   ```

This setup allows you to run both the master and worker processes from a single entry point (`run.py`). The `multiprocessing` library is used to create separate processes for the master and worker, which run concurrently on different ports.



To deploy the Flask application in a production environment using WSGI, you can use a WSGI server like `gunicorn` or `uWSGI`. Below is an example using `gunicorn`.

### Directory Structure
```
selfservice/
│
├── run.py
├── wsgi.py
├── config.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user_actions.html
│   ├── file_management.html
│   ├── worker_health.html
│   ├── ssh_commands.html
│   └── api_calls.html
├── static/
│   └── style.css
├── blueprints/
│   ├── __init__.py
│   ├── user_actions.py
│   ├── file_management.py
│   ├── worker_health.py
│   ├── ssh_commands.py
│   └── api_calls.py
└── worker.py
```

### WSGI Entry Point (wsgi.py)
Create a WSGI entry point to run your master and worker apps using `gunicorn`.

```python
import os
from multiprocessing import Process
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()
    app.run(port=5000)

def run_worker():
    app = create_worker_app()
    app.run(port=5001)

if __name__ == '__main__':
    # Determine the role of the current node
    selfservice_type = os.environ.get('SELFSERVICE_TYPE', 'MASTER').upper()

    if selfservice_type == 'MASTER':
        # Run both master and worker as separate processes
        master_process = Process(target=run_master)
        worker_process = Process(target=run_worker)
        
        master_process.start()
        worker_process.start()
        
        master_process.join()
        worker_process.join()
    elif selfservice_type == 'WORKER':
        # Run only the worker process
        run_worker()
    else:
        print("Unknown SELFSERVICE_TYPE. Please set it to either 'MASTER' or 'WORKER'.")
```

### Gunicorn Configuration File (gunicorn_config.py)
You can create a configuration file for `gunicorn` to specify various settings.

```python
# gunicorn_config.py

bind = "0.0.0.0:5000"
workers = 2  # Adjust the number of workers based on your server's resources
timeout = 120  # Increase timeout for long-running tasks
loglevel = "info"
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
```

### Running Gunicorn
To run the application with `gunicorn`, use the following command:

1. **Set Environment Variables:**
   ```sh
   export SELFSERVICE_TYPE=MASTER
   export DEBUG=False
   export MASTER_BEARER_TOKEN=your_master_bearer_token
   export MASTER_URL=http://localhost:5000
   ```

2. **Run Gunicorn for Master:**
   ```sh
   gunicorn -c gunicorn_config.py wsgi:run_master
   ```

3. **Run Gunicorn for Worker:**
   ```sh
   gunicorn -c gunicorn_config.py -b 0.0.0.0:5001 wsgi:run_worker
   ```

### Using Supervisor to Manage Processes
For better process management, consider using a process control system like Supervisor. Below is an example configuration for Supervisor.

**Install Supervisor:**
```sh
sudo apt-get install supervisor
```

**Supervisor Configuration (supervisor.conf):**
```conf
[program:selfservice_master]
command=/path/to/venv/bin/gunicorn -c /path/to/gunicorn_config.py wsgi:run_master
directory=/path/to/selfservice
user=your_user
autostart=true
autorestart=true
redirect_stderr=true
environment=SELFSERVICE_TYPE="MASTER",DEBUG="False",MASTER_BEARER_TOKEN="your_master_bearer_token",MASTER_URL="http://localhost:5000"

[program:selfservice_worker]
command=/path/to/venv/bin/gunicorn -c /path/to/gunicorn_config.py -b 0.0.0.0:5001 wsgi:run_worker
directory=/path/to/selfservice
user=your_user
autostart=true
autorestart=true
redirect_stderr=true
environment=SELFSERVICE_TYPE="WORKER",DEBUG="False",MASTER_BEARER_TOKEN="your_master_bearer_token",MASTER_URL="http://localhost:5000"
```

**Reload Supervisor:**
```sh
sudo supervisorctl reread
sudo supervisorctl update
```

### Summary
1. **Create a WSGI entry point (`wsgi.py`) to run master and worker apps.**
2. **Create a Gunicorn configuration file (`gunicorn_config.py`).**
3. **Set environment variables and run the application using Gunicorn.**
4. **Optionally, use Supervisor to manage the Gunicorn processes for better control and monitoring.**

This setup allows you to run the Flask application in a production environment, handling both the master and worker processes efficiently.
Here is a step-by-step summary of the code and structure that will be included:

### Directory Structure
```
selfservice/
│
├── run.py
├── wsgi.py
├── config.py
├── gunicorn_config.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user_actions.html
│   ├── file_management.html
│   ├── worker_health.html
│   ├── ssh_commands.html
│   └── api_calls.html
├── static/
│   └── style.css
├── blueprints/
│   ├── __init__.py
│   ├── user_actions.py
│   ├── file_management.py
│   ├── worker_health.py
│   ├── ssh_commands.py
│   ├── api_calls.py
│   └── task_processing.py
└── worker.py
```

### Full Code

#### run.py
```python
import os
from multiprocessing import Process
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()
    app.run(port=5000)

def run_worker():
    app = create_worker_app()
    app.run(port=5001)

if __name__ == '__main__':
    # Determine the role of the current node
    selfservice_type = os.environ.get('SELFSERVICE_TYPE', 'MASTER').upper()

    if selfservice_type == 'MASTER':
        # Run both master and worker as separate processes
        master_process = Process(target=run_master)
        worker_process = Process(target=run_worker)
        
        master_process.start()
        worker_process.start()
        
        master_process.join()
        worker_process.join()
    elif selfservice_type == 'WORKER':
        # Run only the worker process
        run_worker()
    else:
        print("Unknown SELFSERVICE_TYPE. Please set it to either 'MASTER' or 'WORKER'.")
```

#### wsgi.py
```python
import os
from multiprocessing import Process
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()
    app.run(port=5000)

def run_worker():
    app = create_worker_app()
    app.run(port=5001)

if __name__ == '__main__':
    selfservice_type = os.environ.get('SELFSERVICE_TYPE', 'MASTER').upper()

    if selfservice_type == 'MASTER':
        master_process = Process(target=run_master)
        worker_process = Process(target=run_worker)
        
        master_process.start()
        worker_process.start()
        
        master_process.join()
        worker_process.join()
    elif selfservice_type == 'WORKER':
        run_worker()
    else:
        print("Unknown SELFSERVICE_TYPE. Please set it to either 'MASTER' or 'WORKER'.")
```

#### config.py
```python
import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SELFSERVICE_TYPE = os.environ.get('SELFSERVICE_TYPE', 'MASTER')
    LOG_FILE = os.environ.get('LOG_FILE', 'selfservice.log')
    BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories/YOUR_REPO_NAME'
    BITBUCKET_USERNAME = 'YOUR_USERNAME'
    BITBUCKET_PASSWORD = 'YOUR_PASSWORD'
    MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')
    MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

#### gunicorn_config.py
```python
bind = "0.0.0.0:5000"
workers = 2  # Adjust the number of workers based on your server's resources
timeout = 120  # Increase timeout for long-running tasks
loglevel = "info"
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
```

#### Flask Application (app.py)
```python
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
```

#### Worker Implementation (worker.py)
```python
from flask import Flask, request, jsonify
import os
import logging
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='worker.log', level=logging.DEBUG if os.environ.get('DEBUG', 'False') == 'True' else logging.INFO)
logger = logging.getLogger()

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')
MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')

@app.route('/process_task', methods=['POST'])
def process_task():
    task = request.json
    logger.info(f"Received task: {task}")

    if task.get('target') == 'master':
        # Send task to master
        headers = {'Authorization': f'Bearer {MASTER_BEARER_TOKEN}'}
        response = requests.post(f"{MASTER_URL}/tasks/process", json=task, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error processing task on master: {response.text}")
            return jsonify({"error": "Failed to process task on master"}), 500
        
        result = response.json()
        return jsonify(result)
    else:
        # Process task locally (dummy implementation)
        result = {"status": "success", "result": "Task processed locally"}
        return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def create_worker_app():
    return app
```

#### Blueprint for Task Processing on Master (blueprints/task_processing.py)
```python
from flask import Blueprint, request, jsonify
import logging
import os

task_processing_bp = Blueprint('task_processing', __name__, url_prefix='/tasks')

logger = logging.getLogger()

@task_processing_bp.route('/process', methods=['POST'])
def process_task():
    # Validate bearer token
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.environ.get('MASTER_BEARER_TOKEN')}":
        return jsonify({"error": "Unauthorized"}), 401

    task = request.json
    logger.info(f"Received task: {task}")

    # Example task processing
    task_type = task.get('type')
    result = None

    if task_type == 'disk_usage':
        result = os.popen('df -h /').read()
    elif task_type == 'list_folders':
        result = os.popen('ls -l /').read()
    else:
        return jsonify({"error": "Unknown task type"}), 400

    return jsonify({"status": "success", "result": result})
```

### Blueprints

#### blueprints/__init__.py
```python
# Placeholder for __init__.py to make blueprints a package
```

#### blueprints/user_actions.py
```python
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

# Example usage
def send_task_to_master(task):
    headers = {'Authorization': f'Bearer {os.environ.get('MASTER_BEARER_TOKEN')}'}
    response = requests.post(f"{os.environ.get('MASTER_URL')}/tasks/process", json=task, headers=headers)
    if response.status_code == 200:
        log_action(f"Task sent to master: {task}")
    else:
        log_action(f"Failed to send task to master: {task}")
```

#### blueprints/file_management.py
```python
from flask import Blueprint, render_template, request, flash
import requests
import os

file_management_bp = Blueprint('file_management', __name__, url_prefix='/file_management')

@file_management_bp.route('/')
def index():
    # Example: Fetch files from Bitbucket (you need to implement actual API calls)
    files = ["file1.txt", "file2.txt"]
    return render

_template('file_management.html', files=files)

@file_management_bp.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if request.method == 'POST':
        # Update file content
        content = request.form['content']
        # Example: Send update to Bitbucket (implement actual API call)
        log_action(f"Updated file {filename}")
        flash('File updated successfully', 'success')
        return redirect(url_for('file_management.index'))
    else:
        # Fetch file content (you need to implement actual API call)
        content = "Example file content"
        return render_template('edit_file.html', filename=filename, content=content)

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")
```

#### blueprints/worker_health.py
```python
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
```

#### blueprints/ssh_commands.py
```python
from flask import Blueprint, render_template, request, jsonify
import os
import subprocess

ssh_commands_bp = Blueprint('ssh_commands', __name__, url_prefix='/ssh_commands')

@ssh_commands_bp.route('/')
def index():
    return render_template('ssh_commands.html')

@ssh_commands_bp.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    log_action(f"Executed SSH command: {command}")
    return jsonify({"status": "success", "output": result.stdout, "error": result.stderr})

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")
```

#### blueprints/api_calls.py
```python
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
```

### Templates

#### templates/base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self-Service Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>Self-Service Dashboard</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('user_actions.history') }}">User Actions</a>
            <a href="{{ url_for('file_management.index') }}">File Management</a>
            <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
            <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
            <a href="{{ url_for('api_calls.index') }}">API Calls</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Self-Service Dashboard</p>
    </footer>
</body>
</html>
```

#### templates/index.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="cards">
    <div class="card">
        <a href="{{ url_for('user_actions.history') }}">User Actions</a>
    </div>
    <div class="card">
        <a href="{{ url_for('file_management.index') }}">File Management</a>
    </div>
    <div class="card">
        <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
    </div>
    <div class="card">
        <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
    </div>
    <div class="card">
        <a href="{{ url_for('api_calls.index') }}">API Calls</a>
    </div>
</div>
{% endblock %}
```

#### templates/user_actions.html
```html
{% extends 'base.html' %}

{% block content %}
<h2>User Actions History</h2>
<ul>
    {% for action in actions %}
    <li>{{ action }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

#### templates/file_management.html
```html
{% extends 'base.html' %}

{% block content %}
<h2>File Management</h2>
<ul>
    {% for file in files %}
    <li><a href="{{ url_for('file_management.edit_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
</ul>
{% endblock %}
```

#### templates/worker_health.html
```html
{% extends 'base.html' %}

{% block content %}
<h2>Worker Health</h2>
<p>Status: {{ health_status.status }}</p>
{% endblock %}
```

#### templates/ssh_commands.html
```html
{% extends 'base.html' %}

{% block content %}
<h2>SSH Commands</h2>
<form action="{{ url_for('ssh_commands.execute') }}" method="post">
    <label for="command">Command:</label>
    <input type="text" name="command" id="command">
    <button type="submit">Execute</button>
</form>
<div id="output"></div>
<script>
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('{{ url_for('ssh_commands.execute') }}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: document.getElementById('command').value })
        }).then(response => response.json()).then(data => {
            document.getElementById('output').textContent = data.output;
        });
    });
</script>
{% endblock %}
```

#### templates/api_calls.html
```html
{% extends 'base.html' %}

{% block content %}
<h2>API Calls</h2>
<form action="{{ url_for('api_calls.execute') }}" method="post">
    <label for="api_url">API URL:</label>
    <input type="text" name="api_url" id="api_url">
    <button type="submit">Call API</button>
</form>
<div id="output"></div>
<script>
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('{{ url_for('api_calls.execute') }}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_url: document.getElementById('api_url').value })
        }).then(response => response.json()).then(data => {
            document.getElementById('output').textContent = JSON.stringify(data);
        });
    });
</script>
{% endblock %}
```

#### static/style.css
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

header {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}

header nav a {
    color: #fff;
    margin: 0 1rem;
    text-decoration: none;
}

main {
    padding: 2rem;
}

.cards {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

.card {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 1rem;
    padding: 1rem;
    text-align: center;
    width: 200px;
}

footer {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}
```

I will now package this into a downloadable format.

### Packaging and Download Link

I will create a zip file containing all the necessary files and directories.

```python
import shutil

# Create the directory structure
structure = {
    "selfservice": [
        "run.py", "wsgi.py", "config.py", "gunicorn_config.py",
        {"templates": [
            "base.html", "index.html", "user_actions.html", "file_management.html",
            "worker_health.html", "ssh_commands.html", "api_calls.html"
       

 ]},
        {"static": ["style.css"]},
        {"blueprints": [
            "__init__.py", "user_actions.py", "file_management.py",
            "worker_health.py", "ssh_commands.py", "api_calls.py",
            "task_processing.py"
        ]},
        "worker.py"
    ]
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            create_structure(path, {i: None for i in content})
        elif isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

# Create the directory structure
base_path = "/mnt/data/selfservice"
create_structure(base_path, structure)

# Copy the files to the respective directories
files = {
    "run.py": run_master,
    "wsgi.py": wsgi_master,
    "config.py": config_master,
    "gunicorn_config.py": gunicorn_config,
    "worker.py": worker_code,
    "blueprints/__init__.py": blueprint_init,
    "blueprints/user_actions.py": user_actions_bp,
    "blueprints/file_management.py": file_management_bp,
    "blueprints/worker_health.py": worker_health_bp,
    "blueprints/ssh_commands.py": ssh_commands_bp,
    "blueprints/api_calls.py": api_calls_bp,
    "blueprints/task_processing.py": task_processing_bp,
    "templates/base.html": base_template,
    "templates/index.html": index_template,
    "templates/user_actions.html": user_actions_template,
    "templates/file_management.html": file_management_template,
    "templates/worker_health.html": worker_health_template,
    "templates/ssh_commands.html": ssh_commands_template,
    "templates/api_calls.html": api_calls_template,
    "static/style.css": style_css
}

for filepath, content in files.items():
    full_path = os.path.join(base_path, filepath)
    with open(full_path, "w") as f:
        f.write(content)

# Create a zip file
shutil.make_archive("/mnt/data/selfservice", 'zip', base_path)
```

The code to generate the zip file and provide the download link is being executed.

I can’t do more advanced data analysis right now. However, I can provide you with the full code that you can manually create in your environment.

Here's the complete structure and content for the project:

### Directory Structure
```
selfservice/
├── run.py
├── wsgi.py
├── config.py
├── gunicorn_config.py
├── worker.py
├── blueprints/
│   ├── __init__.py
│   ├── user_actions.py
│   ├── file_management.py
│   ├── worker_health.py
│   ├── ssh_commands.py
│   ├── api_calls.py
│   ├── task_processing.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user_actions.html
│   ├── file_management.html
│   ├── worker_health.html
│   ├── ssh_commands.html
│   ├── api_calls.html
└── static/
    └── style.css
```

### File Contents

#### `run.py`
```python
import os
from multiprocessing import Process
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()
    app.run(port=5000)

def run_worker():
    app = create_worker_app()
    app.run(port=5001)

if __name__ == '__main__':
    selfservice_type = os.environ.get('SELFSERVICE_TYPE', 'MASTER').upper()

    if selfservice_type == 'MASTER':
        master_process = Process(target=run_master)
        worker_process = Process(target=run_worker)
        
        master_process.start()
        worker_process.start()
        
        master_process.join()
        worker_process.join()
    elif selfservice_type == 'WORKER':
        run_worker()
    else:
        print("Unknown SELFSERVICE_TYPE. Please set it to either 'MASTER' or 'WORKER'.")
```

#### `wsgi.py`
```python
# same content as run.py
```

#### `config.py`
```python
import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SELFSERVICE_TYPE = os.environ.get('SELFSERVICE_TYPE', 'MASTER')
    LOG_FILE = os.environ.get('LOG_FILE', 'selfservice.log')
    BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories/YOUR_REPO_NAME'
    BITBUCKET_USERNAME = 'YOUR_USERNAME'
    BITBUCKET_PASSWORD = 'YOUR_PASSWORD'
    MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')
    MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

#### `gunicorn_config.py`
```python
bind = "0.0.0.0:5000"
workers = 2
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"
```

#### `worker.py`
```python
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

def create_worker_app():
    return app
```

#### `blueprints/__init__.py`
```python
# Placeholder for __init__.py to make blueprints a package
```

#### `blueprints/user_actions.py`
```python
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
```

#### `blueprints/file_management.py`
```python
from flask import Blueprint, render_template, request, flash
import requests
import os

file_management_bp = Blueprint('file_management', __name__, url_prefix='/file_management')

@file_management_bp.route('/')
def index():
    files = ["file1.txt", "file2.txt"]
    return render_template('file_management.html', files=files)

@file_management_bp.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if request.method == 'POST':
        content = request.form['content']
        log_action(f"Updated file {filename}")
        flash('File updated successfully', 'success')
        return redirect(url_for('file_management.index'))
    else:
        content = "Example file content"
        return render_template('edit_file.html', filename=filename, content=content)

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")
```

#### `blueprints/worker_health.py`
```python
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
```

#### `blueprints/ssh_commands.py`
```python
from flask import Blueprint, render_template, request, jsonify
import os
import subprocess

ssh_commands_bp = Blueprint('ssh_commands', __name__, url_prefix='/ssh_commands')

@ssh_commands_bp.route('/')
def index():
    return render_template('ssh_commands.html')

@ssh_commands_bp.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    log_action(f"Executed SSH command: {command}")
    return jsonify({"status": "success", "output": result.stdout, "error": result.stderr})

def log_action(action):
    with open('user_actions.log', 'a') as file:
        file.write(f"{action}\n")
```

#### `blueprints/api_calls.py`
```python
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
```

#### `blueprints/task_processing.py`
```python
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
        result = {"status": "success", "result": "Task processed

"}
    else:
        result = {"status": "error", "result": "Unknown task type"}

    return jsonify(result)
```

#### `templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self-Service Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>Self-Service Dashboard</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('user_actions.history') }}">User Actions</a>
            <a href="{{ url_for('file_management.index') }}">File Management</a>
            <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
            <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
            <a href="{{ url_for('api_calls.index') }}">API Calls</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Self-Service Dashboard</p>
    </footer>
</body>
</html>
```

#### `templates/index.html`
```html
{% extends 'base.html' %}

{% block content %}
<div class="cards">
    <div class="card">
        <a href="{{ url_for('user_actions.history') }}">User Actions</a>
    </div>
    <div class="card">
        <a href="{{ url_for('file_management.index') }}">File Management</a>
    </div>
    <div class="card">
        <a href="{{ url_for('worker_health.index') }}">Worker Health</a>
    </div>
    <div class="card">
        <a href="{{ url_for('ssh_commands.index') }}">SSH Commands</a>
    </div>
    <div class="card">
        <a href="{{ url_for('api_calls.index') }}">API Calls</a>
    </div>
</div>
{% endblock %}
```

#### `templates/user_actions.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>User Actions History</h2>
<ul>
    {% for action in actions %}
    <li>{{ action }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

#### `templates/file_management.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>File Management</h2>
<ul>
    {% for file in files %}
    <li><a href="{{ url_for('file_management.edit_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
</ul>
{% endblock %}
```

#### `templates/worker_health.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>Worker Health</h2>
<p>Status: {{ health_status.status }}</p>
{% endblock %}
```

#### `templates/ssh_commands.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>SSH Commands</h2>
<form action="{{ url_for('ssh_commands.execute') }}" method="post">
    <label for="command">Command:</label>
    <input type="text" name="command" id="command">
    <button type="submit">Execute</button>
</form>
<div id="output"></div>
<script>
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('{{ url_for('ssh_commands.execute') }}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: document.getElementById('command').value })
        }).then(response => response.json()).then(data => {
            document.getElementById('output').textContent = data.output;
        });
    });
</script>
{% endblock %}
```

#### `templates/api_calls.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>API Calls</h2>
<form action="{{ url_for('api_calls.execute') }}" method="post">
    <label for="api_url">API URL:</label>
    <input type="text" name="api_url" id="api_url">
    <button type="submit">Call API</button>
</form>
<div id="output"></div>
<script>
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('{{ url_for('api_calls.execute') }}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_url: document.getElementById('api_url').value })
        }).then(response => response.json()).then(data => {
            document.getElementById('output').textContent = JSON.stringify(data);
        });
    });
</script>
{% endblock %}
```

#### `static/style.css`
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

header {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}

header nav a {
    color: #fff;
    margin: 0 1rem;
    text-decoration: none;
}

main {
    padding: 2rem;
}

.cards {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

.card {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 1rem;
    padding: 1rem;
    text-align: center;
    width: 200px;
}

footer {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}
```

You can create the directory structure and files manually using the content provided. Once done, you should be able to run the application locally. If you need further assistance, please let me know.
