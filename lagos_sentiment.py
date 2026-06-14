import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Lagos Politics Sentiment", layout="wide")
st.title("🗳️ Lagos State Politics Sentiment Tracker")
st.markdown("Track governorship, candidates (Hamzat, Rhodes-Vivour, etc.), economy, grassroots opinions on X.")

# Sample data for testing
@st.cache_data
def load_sample():
    return pd.DataFrame([
        {"text": "Hamzat is doing great for Lagos economy and development!", "created_at": "2026-06-01"},
        {"text": "Waste everywhere, APC failing grassroots people in Lagos.", "created_at": "2026-06-05"},
        {"text": "We need better roads and jobs from the next governor.", "created_at": "2026-06-10"},
        {"text": "Rhodes-Vivour understands people's needs better.", "created_at": "2026-06-12"},
        {"text": "Politics in Lagos is full of bias and emotional support for parties.", "created_at": "2026-06-13"},
        {"text": "Lagos economy is suffering, we want real change now!", "created_at": "2026-06-14"},
    ])

df = load_sample()

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return 'Positive', compound
    elif compound <= -0.05:
        return 'Negative', compound
    else:
        return 'Neutral', compound

df[['sentiment', 'score']] = df['text'].apply(lambda x: pd.Series(get_sentiment(x)))

# Calculate percentages
counts = df['sentiment'].value_counts()
total = len(df)
percentages = (counts / total * 100).round(2)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Overall Sentiment")
    fig = px.pie(names=percentages.index, values=percentages.values, 
                 color=percentages.index, 
                 color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
    st.plotly_chart(fig)

with col2:
    st.subheader("Summary")
    st.metric("Positive", f"{percentages.get('Positive', 0)}%")
    st.metric("Negative", f"{percentages.get('Negative', 0)}%")
    st.metric("Neutral", f"{percentages.get('Neutral', 0)}%")

st.subheader("Sample Tweets Analyzed")
st.dataframe(df[['text', 'sentiment']])

# Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Results as CSV", csv, "lagos_sentiment_sample.csv", "text/csv")
