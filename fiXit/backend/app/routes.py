# backend/app/routes.py

from flask import Blueprint, request, jsonify, current_app
from backend.app.services.file_service import save_file, read_file
from backend.app.services.sentiment_service import analyze_sentiment
import os

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = save_file(file)
        return jsonify({'file_id': filename}), 200

@main.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if 'text' in data:
        text = data['text']
    elif 'file_id' in data:
        file_id = data['file_id']
        text = read_file(file_id)
    else:
        return jsonify({'error': 'No text or file_id provided'}), 400

    file_size = len(text)
    sentiment_result = analyze_sentiment(text)
    result = {
        'filename': 'Pasted text' if 'text' in data else data['file_id'],
        'file_size': file_size,
        'text': text,
        'word_count': len(text.split()),
        'char_count': len(text),
        **sentiment_result
    }
    return jsonify(result), 200

@main.route('/results', methods=['GET'])
def get_results():
    results = []
    upload_folder = current_app.config['UPLOAD_FOLDER']
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        text = read_file(filename)
        file_size = os.path.getsize(file_path)
        sentiment_result = analyze_sentiment(text)
        results.append({
            'filename': filename,
            'file_size': file_size,
            'text': text,
            'word_count': len(text.split()),  # Add this line
            'char_count': len(text),
            **sentiment_result
        })
    return jsonify(results), 200

