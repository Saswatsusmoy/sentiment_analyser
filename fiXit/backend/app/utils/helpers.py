# backend/app/utils/helpers.py

import os
import sys

from flask import current_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_upload_folder_exists(app):
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

def read_file(file_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_id)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
