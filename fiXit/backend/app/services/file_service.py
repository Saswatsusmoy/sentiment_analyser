# backend/app/services/file_service.py

import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename

def read_file(file_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_id)
    with open(file_path, 'r') as file:
        return file.read()
