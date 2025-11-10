import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Lloyds Customer Segments",
    page_icon="💳",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILE = DATA_DIR / "customer_segments.csv"

SEGMENT_LABELS = {
    0: "High Value",
    1: "Budget Conscious",
    2: "Family Focused",
    3: "Growth Potential",
}

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["ClusterName"] = df["Cluster"].map(SEGMENT_LABELS).fillna("Unknown")
    return df

df = load_data()

st.title("💳 Lloyds Bank Customer Segmentation Dashboard")
st.markdown("Interactively explore customer clusters derived from the Lloyds analytics notebook.")

st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=list(sorted(df["Gender"].unique())),
)

income_filter = st.sidebar.multiselect(
    "Income Level",
    options=sorted(df["IncomeLevel"].unique()),
    default=list(sorted(df["IncomeLevel"].unique())),
)

cluster_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["ClusterName"].unique()),
    default=list(sorted(df["ClusterName"].unique())),
)

filtered_df = df[
    df["Gender"].isin(gender_filter)
    & df["IncomeLevel"].isin(income_filter)
    & df["ClusterName"].isin(cluster_filter)
]
if filtered_df.empty:
    st.warning("No customers match the current filter selection.")
else:
    st.subheader("Customer Snapshot")
    col1, col2, col3 = st.columns(3)
    avg_age = filtered_df["Age"].mean() if not filtered_df.empty else 0
    income_mix = ", ".join(sorted(filtered_df["IncomeLevel"].unique())) or "N/A"
    col1.metric("Customers", f"{len(filtered_df):,}")
    col2.metric("Average Age", f"{avg_age:.1f} yrs")
    col3.metric("Income Mix", income_mix)

    st.markdown("### Segment Distribution")
    segment_counts = (
        filtered_df["ClusterName"].value_counts(normalize=True).rename_axis("Segment").reset_index(name="Share")
    )
    fig_segments = px.pie(
        segment_counts,
        names="Segment",
        values="Share",
        title="Share of customers by segment",
    )
    st.plotly_chart(fig_segments, use_container_width=True)

    st.markdown("### Age by Segment")
    fig_age = px.box(
        filtered_df,
        x="ClusterName",
        y="Age",
        color="ClusterName",
        title="Age distribution per segment",
        labels={"ClusterName": "Segment", "Age": "Age"},
    )
    fig_age.update_layout(showlegend=False)
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("### Gender & Income Composition")
    composition = (
        filtered_df.groupby(["ClusterName", "Gender", "IncomeLevel"]).size().reset_index(name="Customers")
    )
    fig_heatmap = px.density_heatmap(
        composition,
        x="Gender",
        y="ClusterName",
        z="Customers",
        facet_col="IncomeLevel",
        color_continuous_scale="Blues",
        title="Customer count by gender, segment, and income",
    )
    fig_heatmap.update_layout(height=500)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    with st.expander("📋 Customer Table"):
        st.dataframe(
            filtered_df[["CustomerID", "Age", "Gender", "MaritalStatus", "IncomeLevel", "ClusterName"]]
            .rename(columns={"ClusterName": "Segment"})
            .sort_values("CustomerID"),
            use_container_width=True,
        )

st.caption("Data source: Lloyds Bank customer segmentation notebook outputs.")
