# frontend/pages/home.py

import streamlit as st
from utils.api import upload_file, analyze_sentiment, get_all_results
import pandas as pd

def app():
    st.title("Sentiment Analysis App")
    
    # Add a text area for pasting text
    text_input = st.text_area("Enter text for sentiment analysis:", height=200)
    
    # File uploader
    uploaded_file = st.file_uploader("Or choose a file for analysis", type=['txt', 'pdf'])
    
    if st.button("Analyze Sentiment"):
        with st.spinner("Analyzing..."):
            if text_input:
                # Analyze pasted text
                result = analyze_sentiment(text_input)
            elif uploaded_file is not None:
                # Upload and analyze file
                file_id = upload_file(uploaded_file)
                if file_id:
                    result = analyze_sentiment(file_id)
                else:
                    st.error("Failed to upload file. Please try again.")
                    return
            else:
                st.warning("Please enter text or upload a file for analysis.")
                return
            
            if result:
                display_result(result)
            else:
                st.error("Failed to analyze sentiment. Please try again.")

def display_result(result):
    results = get_all_results()
    
    if results:
        df = pd.DataFrame(results)
        
        # Display sentiment scores and counts
        st.subheader("Sentiment Scores and Text Statistics")
        for index, row in df.iterrows():
            st.write(f"File: {row['filename']}")
            st.write(f"Sentiment: {row['sentiment']}")
            st.write(f"Positive Score: {row['pos_score']:.2f}")
            st.write(f"Negative Score: {row['neg_score']:.2f}")
            st.write(f"Neutral Score: {row['neu_score']:.2f}")
            st.write(f"Compound Score: {row['compound_score']:.2f}")
            if 'word_count' in row:
                st.write(f"Word Count: {row['word_count']}")
            if 'char_count' in row:
                st.write(f"Character Count: {row['char_count']}")
            st.write("---")
