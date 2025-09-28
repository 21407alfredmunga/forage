import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Social Buzz Content Dashboard",
    page_icon="📊",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@st.cache_data
def load_data():
    interactions = pd.read_csv(DATA_DIR / "merged_top_5_dataframe.csv", parse_dates=["Datetime"])
    top_categories = pd.read_csv(DATA_DIR / "top_5_categories.csv")
    return interactions, top_categories

interactions_df, top_categories_df = load_data()

st.title("📊 Social Buzz Content Performance")
st.markdown(
    "Use this dashboard to explore how the top-performing content categories on Social Buzz are engaging customers."
)

st.sidebar.header("Controls")
category_options = ["All"] + sorted(interactions_df["Category"].unique())
selected_category = st.sidebar.selectbox("Select Category", category_options)

if selected_category != "All":
    filtered_df = interactions_df[interactions_df["Category"] == selected_category]
else:
    filtered_df = interactions_df.copy()

# Key metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Interactions", f"{len(filtered_df):,}")
avg_score = filtered_df["Score_final"].mean() if not filtered_df.empty else 0
positive_share = (
    (filtered_df["Sentiment"].str.lower() == "positive").mean() if not filtered_df.empty else 0
)
col2.metric("Average Sentiment Score", f"{avg_score:.1f}")
col3.metric("Positive Share", f"{positive_share:.0%}")

# Category leaderboard
st.markdown("### 🏆 Top Content Categories")
leaderboard = top_categories_df.sort_values("Score", ascending=False)
st.dataframe(leaderboard, use_container_width=True)

# Sentiment distribution
st.markdown("### 😊 Sentiment Distribution")
sentiment_counts = (
    filtered_df["Sentiment"]
    .str.title()
    .value_counts()
    .rename_axis("Sentiment")
    .reset_index(name="Count")
)

fig_sentiment = px.bar(
    sentiment_counts,
    x="Sentiment",
    y="Count",
    color="Sentiment",
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="Sentiment Breakdown",
)
fig_sentiment.update_layout(showlegend=False)
st.plotly_chart(fig_sentiment, use_container_width=True)

# Engagement over time
st.markdown("### ⏱ Engagement Over Time")
timeframe = st.sidebar.selectbox("Time Granularity", ["Daily", "Weekly", "Monthly"], index=2)

if timeframe == "Daily":
    timeline = filtered_df.set_index("Datetime").resample("D")
elif timeframe == "Weekly":
    timeline = filtered_df.set_index("Datetime").resample("W")
else:
    timeline = filtered_df.set_index("Datetime").resample("M")

timeline_df = timeline["Score_final"].sum().reset_index()
timeline_df["Datetime"] = timeline_df["Datetime"].dt.date

fig_timeline = px.line(
    timeline_df,
    x="Datetime",
    y="Score_final",
    markers=True,
    title="Total Interaction Score Over Time",
)
fig_timeline.update_traces(line_color="#636EFA")
st.plotly_chart(fig_timeline, use_container_width=True)

# Raw data option
with st.expander("🔍 Explore Raw Data"):
    st.dataframe(filtered_df.sort_values("Datetime", ascending=False), use_container_width=True)

st.caption("Data source: Social Buzz top 5 content categories analysis notebook.")
