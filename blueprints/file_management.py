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