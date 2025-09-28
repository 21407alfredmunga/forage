import streamlit as st
import pandas as pd
from pathlib import Path
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px

st.set_page_config(
    page_title="British Airways Review Insights",
    page_icon="✈️",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@st.cache_resource
def load_analyzer():
    nltk.download("vader_lexicon", quiet=True)
    return SentimentIntensityAnalyzer()

@st.cache_data
def load_reviews():
    csv_path = DATA_DIR / "BA_reviews_cleaned.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "BA_reviews.csv"
    df = pd.read_csv(csv_path)
    if "reviews" not in df.columns:
        raise ValueError("Expected a 'reviews' column in the dataset.")
    df = df.rename(columns={df.columns[0]: "index"}).drop(columns=["index"], errors="ignore")
    df["Review"] = df["reviews"].astype(str).str.strip()
    df["is_verified"] = df["Review"].str.contains("Trip Verified", case=False)
    df["verification_label"] = df["is_verified"].map({True: "Trip Verified", False: "Not Verified"})
    df["clean_review"] = (
        df["Review"]
        .str.replace(r"✅ Trip Verified \|", "", regex=True)
        .str.replace(r"Not Verified \|", "", regex=True)
        .str.strip()
    )
    df["word_count"] = df["clean_review"].str.split().apply(len)
    return df

sia = load_analyzer()
reviews_df = load_reviews()

@st.cache_data
def score_sentiment(text_series: pd.Series) -> pd.DataFrame:
    scores = text_series.apply(lambda txt: sia.polarity_scores(txt)["compound"])
    sentiment_df = pd.DataFrame({"compound": scores})
    sentiment_df["sentiment_label"] = pd.cut(
        sentiment_df["compound"],
        bins=[-1.01, -0.05, 0.05, 1.01],
        labels=["Negative", "Neutral", "Positive"],
    )
    return sentiment_df

sentiment_scores = score_sentiment(reviews_df["clean_review"])
reviews_df = pd.concat([reviews_df, sentiment_scores], axis=1)

st.title("✈️ British Airways Customer Feedback Dashboard")
st.markdown(
    "Analyze customer sentiment for British Airways based on reviews collected from Skytrax."
)

st.sidebar.header("Filters")
verification_filter = st.sidebar.multiselect(
    "Verification status",
    options=sorted(reviews_df["verification_label"].unique()),
    default=list(reviews_df["verification_label"].unique()),
)

sentiment_filter = st.sidebar.multiselect(
    "Sentiment",
    options=["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"],
)

word_min = int(reviews_df["word_count"].min())
word_max = int(reviews_df["word_count"].max())
default_low = max(word_min, 50)
min_words, max_words = st.sidebar.slider(
    "Word count range",
    word_min,
    word_max,
    (default_low, word_max),
)

filtered_df = reviews_df[
    (reviews_df["verification_label"].isin(verification_filter))
    & (reviews_df["sentiment_label"].isin(sentiment_filter))
    & (reviews_df["word_count"].between(min_words, max_words))
]

if filtered_df.empty:
    st.warning("No reviews match the current filter selection.")
else:
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews Displayed", f"{len(filtered_df):,}")
    avg_compound = filtered_df["compound"].mean() if not filtered_df.empty else 0
    positive_share = (
        (filtered_df["sentiment_label"] == "Positive").mean() if not filtered_df.empty else 0
    )
    col2.metric("Avg. Sentiment (compound)", f"{avg_compound:.2f}")
    col3.metric("Positive Share", f"{positive_share:.0%}")

    st.markdown("### Sentiment Distribution")
    sentiment_counts = (
        filtered_df["sentiment_label"].value_counts(normalize=False).sort_index()
    )
    fig_sentiment = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        color=sentiment_counts.index,
        color_discrete_map={"Positive": "#2ca02c", "Neutral": "#ff7f0e", "Negative": "#d62728"},
    )
    fig_sentiment.update_layout(title="Sentiment Share", legend_title="Sentiment")
    st.plotly_chart(fig_sentiment, use_container_width=True)

    st.markdown("### Verification Breakdown")
    verification_summary = (
        filtered_df.groupby(["verification_label", "sentiment_label"]).size().reset_index(name="count")
    )
    fig_verification = px.bar(
        verification_summary,
        x="verification_label",
        y="count",
        color="sentiment_label",
        barmode="stack",
        color_discrete_map={"Positive": "#2ca02c", "Neutral": "#ff7f0e", "Negative": "#d62728"},
        title="Sentiment by Verification Status",
    )
    fig_verification.update_layout(xaxis_title="Verification Status", yaxis_title="Number of Reviews")
    st.plotly_chart(fig_verification, use_container_width=True)

    st.markdown("### Longest & Shortest Reviews")
    col_left, col_right = st.columns(2)
    with col_left:
        longest_review = filtered_df.sort_values("word_count", ascending=False).head(1)
        if not longest_review.empty:
            st.write("**Longest Review**")
            st.info(longest_review["clean_review"].iloc[0])
            st.caption(f"Word count: {longest_review['word_count'].iloc[0]}")
    with col_right:
        shortest_review = filtered_df.sort_values("word_count", ascending=True).head(1)
        if not shortest_review.empty:
            st.write("**Shortest Review**")
            st.info(shortest_review["clean_review"].iloc[0])
            st.caption(f"Word count: {shortest_review['word_count'].iloc[0]}")

    with st.expander("🔎 Explore Reviews"):
        st.dataframe(
            filtered_df[["verification_label", "sentiment_label", "compound", "word_count", "clean_review"]]
            .rename(columns={
                "verification_label": "Verification",
                "sentiment_label": "Sentiment",
                "compound": "Compound Score",
                "word_count": "Word Count",
                "clean_review": "Review",
            })
            .sort_values("Compound Score", ascending=False),
            use_container_width=True,
        )

st.caption("Data source: Scraped British Airways customer reviews. Sentiment scored with NLTK VADER.")
