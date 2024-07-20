# frontend/utils/api.py

import requests
import streamlit as st

BASE_URL = "http://localhost:5000"  # Adjust this to your backend URL

def upload_file(file):
    response = requests.post(f"{BASE_URL}/upload", files={"file": file})
    if response.status_code == 200:
        data = response.json()
        return data.get("file_id")
    else:
        st.error(f"Error uploading file: {response.status_code}")
        return None

def analyze_sentiment(input_data):
    if isinstance(input_data, str):
        # If input_data is a string, it's pasted text
        response = requests.post(f"{BASE_URL}/analyze", json={"text": input_data})
    else:
        # Otherwise, it's a file_id
        response = requests.post(f"{BASE_URL}/analyze", json={"file_id": input_data})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error analyzing sentiment: {response.status_code}")
        return None

def get_all_results():
    response = requests.get(f"{BASE_URL}/results")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching results: {response.status_code}")
        return None
