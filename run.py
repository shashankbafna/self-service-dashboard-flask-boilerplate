import os
from multiprocessing import Process
from flask import Flask, request
from app import create_app
from worker import create_worker_app

def run_master():
    app = create_app()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'

    app.run(port=5000)

def run_worker():
    app = create_worker_app()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'

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
