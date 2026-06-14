import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px

st.set_page_config(page_title="Hamzat 2027 Sentiment Intelligence", layout="wide")

st.title("🗳️ Hamzat 2027 Lagos Governorship Sentiment Intelligence Platform")
st.markdown("**Built by Babajide Owolodun** | Strategic Public Opinion & Political Intelligence Dashboard")

st.markdown("---")

# File Upload
uploaded_file = st.file_uploader("📤 Upload Tweets CSV from Apify", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} tweets")
else:
    df = pd.DataFrame([
        {"text": "Hamzat is the best choice for continuity and development in Lagos", "created_at": "2026-06-01"},
        {"text": "Waste management crisis under current leadership", "created_at": "2026-06-05"},
    ])

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()
def get_sentiment(text):
    scores = analyzer.polarity_scores(str(text))
    compound = scores['compound']
    if compound >= 0.05: return 'Positive', compound
    elif compound <= -0.05: return 'Negative', compound
    else: return 'Neutral', compound

df[['sentiment', 'score']] = df['text'].apply(lambda x: pd.Series(get_sentiment(x)))

# Always Visible Overall Sentiment (Top of Page)
st.subheader("📊 Overall Sentiment Analysis")
counts = df['sentiment'].value_counts()
total = len(df)
percentages = (counts / total * 100).round(2)

col1, col2 = st.columns([3, 2])
with col1:
    fig = px.pie(names=percentages.index, values=percentages.values,
                 color=percentages.index,
                 color_discrete_map={'Positive':'#00C853','Negative':'#FF1744','Neutral':'#78909C'},
                 title="Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Positive", f"{percentages.get('Positive', 0)}%")
    st.metric("Negative", f"{percentages.get('Negative', 0)}%")
    st.metric("Neutral", f"{percentages.get('Neutral', 0)}%")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Hamzat Specific", "Leadership & Trust", "Economy, Youth & Stakeholders", "Strategic Insights"])

with tab1:
    st.subheader("Dr. Kadri Obafemi Hamzat Sentiment")
    hamzat_df = df[df['text'].str.contains('Hamzat|Obafemi|KOH|Kadri', case=False, na=False)]
    st.write(f"**Tweets mentioning Hamzat**: {len(hamzat_df)}")
    if len(hamzat_df) > 0:
        h_counts = hamzat_df['sentiment'].value_counts()
        h_total = len(hamzat_df)
        h_perc = (h_counts / h_total * 100).round(2)
        st.plotly_chart(px.pie(names=h_perc.index, values=h_perc.values, color_discrete_map={'Positive':'#00C853','Negative':'#FF1744','Neutral':'#78909C'}))

with tab2:
    st.subheader("Leadership Success & Public Trust")
    leadership_kw = ['leadership', 'trust', 'vision', 'continuity', 'governance', 'performance']
    for kw in leadership_kw:
        score = len(df[df['text'].str.contains(kw, case=False, na=False)])
        st.write(f"• **{kw.capitalize()}** mentions: {score}")

with tab3:
    st.subheader("Economy, Youth, Business, Investors & Diaspora")
    econ_kw = ['economy', 'youth', 'jobs', 'business', 'investor', 'diaspora', 'inclusi']
    for kw in econ_kw:
        score = len(df[df['text'].str.contains(kw, case=False, na=False)])
        st.write(f"• **{kw.capitalize()}** alignment mentions: {score}")

with tab4:
    st.subheader("Strategic Recommendations")
    st.markdown("""
    **Key Actions for 2027 Victory:**
    - Address top negative themes immediately (e.g. waste, cost of living)
    - Amplify success stories on infrastructure, digital transformation and youth empowerment
    - Build coalition with business, youth and diaspora communities
    - Publish regular "State of Public Alignment" reports
    """)

# Full Data
st.subheader("Recent Tweets Analyzed")
st.dataframe(df[['text', 'sentiment']].head(50))

# Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Full Strategic Report (CSV)", csv, "hamzat_2027_sentiment_report.csv")
