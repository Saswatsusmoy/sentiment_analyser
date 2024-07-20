# frontend/pages/results.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from utils.api import get_all_results

def app():
    st.title("Analysis Results")
    
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
        
        # Pie chart for sentiment distribution
        sentiment_counts = df['sentiment'].value_counts()
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Bar chart for average scores
        avg_scores = df[['pos_score', 'neg_score', 'neu_score']].mean()
        fig_bar = px.bar(
            x=avg_scores.index,
            y=avg_scores.values,
            title="Average Sentiment Scores",
            labels={'x': 'Sentiment Type', 'y': 'Average Score'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Scatter plot for compound score vs. word count
        fig_scatter = px.scatter(
            df,
            x='word_count',
            y='compound_score',
            hover_data=['filename'],
            title="Compound Score vs. Word Count",
            labels={'word_count': 'Word Count', 'compound_score': 'Compound Score'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # New visualizations
        
        # Word frequency
        all_words = ' '.join(df['text']).lower().split()
        word_freq = Counter(all_words)
        common_words = word_freq.most_common(20)
        
        fig_word_freq = px.bar(
            x=[word for word, _ in common_words],
            y=[count for _, count in common_words],
            title="Top 20 Most Frequent Words",
            labels={'x': 'Word', 'y': 'Frequency'}
        )
        st.plotly_chart(fig_word_freq, use_container_width=True)
        
        # Word contribution to sentiment
        word_sentiment = {}
        for _, row in df.iterrows():
            words = row['text'].lower().split()
            sentiment = row['sentiment'].lower()
            for word in set(words):
                if word not in word_sentiment:
                    word_sentiment[word] = {'positive': 0, 'negative': 0, 'neutral': 0, 'count': 0}
                if sentiment == 'positive':
                    word_sentiment[word]['positive'] += 1
                elif sentiment == 'negative':
                    word_sentiment[word]['negative'] += 1
                else:
                    word_sentiment[word]['neutral'] += 1
                word_sentiment[word]['count'] += 1

        top_words = sorted(word_sentiment.items(), key=lambda x: x[1]['count'], reverse=True)[:20]

        fig_word_sentiment = go.Figure()
        for sentiment in ['positive', 'negative', 'neutral']:
            fig_word_sentiment.add_trace(go.Bar(
                x=[word for word, _ in top_words],
                y=[data[sentiment] / data['count'] for _, data in top_words],
                name=sentiment.capitalize()
            ))

        fig_word_sentiment.update_layout(
            title="Top 20 Words' Contribution to Sentiment",
            xaxis_title="Word",
            yaxis_title="Proportion",
            barmode='stack'
        )
        st.plotly_chart(fig_word_sentiment, use_container_width=True)
        
    else:
        st.info("No results available yet.")
