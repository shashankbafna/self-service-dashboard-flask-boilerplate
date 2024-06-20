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


**Solution**
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

By following this approach, the worker can send tasks to the master, which processes them and returns the results. The communication is secured using bearer tokens, and user actions are logged for auditing purposes.

To run both the master and worker instances from a single `run.py` file, you can use `multiprocessing` or `threading` to start both Flask applications simultaneously. Here, we'll use `multiprocessing` to achieve this.

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
I can’t do more advanced data analysis right now. However, I can provide you with the full code that you can manually create in your environment.

To gracefully stop the Flask server and any running processes associated with it, you can follow these steps:

### 1. Using Keyboard Interrupt
When running the Flask application via the command line, you can stop the server by pressing `Ctrl+C`. This sends a SIGINT (interrupt signal) to the process, which will shut down the server.

### 2. Stopping the Server Programmatically
You can implement an endpoint to shutdown the server programmatically. This can be useful for automated testing or other use cases where you need to control the server lifecycle from within the application.

### 3. Sending Shutdown Request
To shut down the server, you can use a tool like `curl`, Postman, or any HTTP client to send a POST request to the `/shutdown` endpoint.

For the master server:
```bash
curl -X POST http://localhost:5000/shutdown
```

For the worker server:
```bash
curl -X POST http://localhost:5001/shutdown
```

### Note:
- These shutdown endpoints should be secured and used with caution, especially in a production environment. Consider adding authentication and authorization checks before allowing the shutdown request to be processed.
- In production, you typically manage the server lifecycle using process managers like `systemd`, `supervisord`, or container orchestration tools like Kubernetes. These tools provide more robust ways to start, stop, and monitor your services.

Here's the complete structure and content for the project:

### Directory Structure
```
selfservice/
├── app.py
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
