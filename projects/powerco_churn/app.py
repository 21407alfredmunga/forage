import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="PowerCo Churn Explorer",
    page_icon="⚡",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILE = DATA_DIR / "clean_data_after_eda.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date_activ", "date_end", "date_modif_prod", "date_renewal"], infer_datetime_format=True)
    df["has_gas"] = df["has_gas"].map({"t": "Yes", "f": "No"})
    df["churn_label"] = df["churn"].map({1: "Churned", 0: "Active"})
    return df

df = load_data()

st.title("⚡ PowerCo Customer Churn Dashboard")
st.markdown(
    "Explore drivers behind customer churn and identify customer segments at risk."
)

st.sidebar.header("Filters")

has_gas_options = sorted(df["has_gas"].dropna().unique())
selected_gas = st.sidebar.multiselect("Gas Subscription", has_gas_options, default=has_gas_options)

product_range = st.sidebar.slider(
    "Number of Active Products",
    int(df["nb_prod_act"].min()),
    int(df["nb_prod_act"].max()),
    (int(df["nb_prod_act"].min()), int(df["nb_prod_act"].max())),
)

origin_options = sorted(df["origin_up"].dropna().unique())
selected_origins = st.sidebar.multiselect("Acquisition Channel", origin_options, default=origin_options)

filtered_df = df[
    df["has_gas"].isin(selected_gas)
    & df["nb_prod_act"].between(*product_range)
    & df["origin_up"].isin(selected_origins)
]

if filtered_df.empty:
    st.warning("No customers match the current filter selection.")
else:
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    churn_rate = filtered_df["churn"].mean() if not filtered_df.empty else 0
    avg_margin = filtered_df["margin_net_pow_ele"].mean() if not filtered_df.empty else 0
    col1.metric("Customers", f"{len(filtered_df):,}")
    col2.metric("Churn Rate", f"{churn_rate:.0%}")
    col3.metric("Avg. Net Margin (€)", f"{avg_margin:.2f}")

    st.markdown("### Churn by Acquisition Channel")
    channel_churn = (
        filtered_df.groupby("origin_up")["churn"].mean().reset_index()
        .sort_values("churn", ascending=False)
    )
    fig_channel = px.bar(
        channel_churn,
        x="origin_up",
        y="churn",
        title="Average churn probability by channel",
        labels={"origin_up": "Channel", "churn": "Churn Rate"},
        color="churn",
        color_continuous_scale="Reds",
    )
    fig_channel.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("### Consumption vs. Net Margin")
    fig_scatter = px.scatter(
        filtered_df,
        x="cons_12m",
        y="margin_net_pow_ele",
        color="churn_label",
        size="pow_max",
        marginal_x="box",
        marginal_y="violin",
        labels={
            "cons_12m": "Consumption (12m)",
            "margin_net_pow_ele": "Net Margin (€)",
            "churn_label": "Status",
            "pow_max": "Max Power",
        },
        title="Customer profitability vs. consumption",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### Churn Cohort by Activation Year")
    cohort_df = filtered_df.copy()
    cohort_df["activation_year"] = cohort_df["date_activ"].dt.year
    cohort_summary = cohort_df.groupby(["activation_year", "churn_label"]).size().reset_index(name="customers")
    fig_cohort = px.bar(
        cohort_summary,
        x="activation_year",
        y="customers",
        color="churn_label",
        barmode="stack",
        title="Customer status by activation year",
        labels={"activation_year": "Activation Year", "customers": "Customers"},
        color_discrete_map={"Active": "#1f77b4", "Churned": "#d62728"},
    )
    fig_cohort.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_cohort, use_container_width=True)

    with st.expander("🔍 View Filtered Data"):
        display_cols = [
            "churn_label",
            "has_gas",
            "nb_prod_act",
            "origin_up",
            "cons_12m",
            "margin_net_pow_ele",
            "pow_max",
            "date_activ",
            "date_renewal",
        ]
        st.dataframe(
            filtered_df[display_cols].sort_values("margin_net_pow_ele", ascending=False),
            use_container_width=True,
        )

st.caption("Data source: PowerCo customer churn notebook outputs.")
