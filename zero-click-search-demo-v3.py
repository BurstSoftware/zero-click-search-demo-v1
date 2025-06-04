import streamlit as st
import plotly.express as px
import pandas as pd
from pytrends.request import TrendReq
import time

# Set page title and layout
st.set_page_config(page_title="Zero-Click & Search Trends Demo", layout="centered")

# Initialize pytrends
try:
    pytrends = TrendReq(hl='en-US', tz=360)
except Exception as e:
    st.error(f"Error initializing Google Trends: {e}")
    pytrends = None

# Title
st.title("Zero-Click Search & Search Volume Trends")

# Zero-Click Explanation
st.write("""
According to a recent Bain survey, **80% of consumers** rely on **zero-click results** 
in at least **40% of their searches**. This means they get their answers directly 
on the search engine results page (SERP) without clicking through to a website.
""")

# Zero-Click Data Visualization
zero_click_data = {
    "Category": ["Consumers Using Zero-Click", "Searches with Zero-Click"],
    "Percentage": [80, 40]
}
df_zero_click = pd.DataFrame(zero_click_data)

fig_zero_click = px.bar(
    df_zero_click,
    x="Category",
    y="Percentage",
    text="Percentage",
    title="Zero-Click Search Statistics (Bain Survey)",
    labels={"Percentage": "Percentage (%)"},
    color="Category",
    color_discrete_map={
        "Consumers Using Zero-Click": "#1f77b4",
        "Searches with Zero-Click": "#ff7f0e"
    }
)
fig_zero_click.update_traces(texttemplate="%{text}%", textposition="auto")
fig_zero_click.update_layout(showlegend=False, yaxis_range=[0, 100])

st.plotly_chart(fig_zero_click, use_container_width=True)

# Sample Dataset for Fallback
sample_data = {
    "Search Term": ["best laptops", "best laptops", "best laptops", "python tutorial", "python tutorial", "python tutorial"],
    "Month": ["2025-01", "2025-02", "2025-03", "2025-01", "2025-02", "2025-03"],
    "Search Volume": [120000, 130000, 125000, 80000, 85000, 90000]
}
df_search = pd.DataFrame(sample_data)

# Save sample dataset to a CSV file for demonstration
df_search.to_csv("search_volume_data.csv", index=False)

# Load fallback dataset
try:
    df_search = pd.read_csv("search_volume_data.csv")
except FileNotFoundError:
    st.error("Search volume dataset not found. Using sample data.")
    df_search = pd.DataFrame(sample_data)

# API Key Input
st.subheader("Google Trends Integration")
api_key = st.text_input("Enter your Google API Key (optional for Google Trends)", type="password")
st.write("Note: Google Trends via pytrends does not require an API key, but you can enter one if using a different Google API.")

# Search Term Input
st.subheader("Explore Monthly Search Volume Trends")
selected_term = st.text_input("Enter a search term to query Google Trends", "")

# Fetch and Visualize Google Trends Data
if selected_term and pytrends:
    st.write(f"Fetching Google Trends data for '{selected_term}'...")
    try:
        pytrends.build_payload(kw_list=[selected_term], timeframe='today 3-m', geo='US')
        trends_data = pytrends.interest_over_time()
        if selected_term in trends_data.columns and not trends_data.empty:
            trends_df = trends_data[[selected_term]].reset_index()
            trends_df.columns = ["Month", "Search Interest"]
            trends_df["Month"] = trends_df["Month"].dt.strftime("%Y-%m")
            trends_df["Search Term"] = selected_term

            # Visualize Trends Data
            fig_trends = px.line(
                trends_df,
                x="Month",
                y="Search Interest",
                title=f"Google Trends Interest for '{selected_term}' (Last 3 Months)",
                labels={"Search Interest": "Relative Search Interest (0-100)"},
                markers=True
            )
            fig_trends.update_layout(yaxis_title="Search Interest", xaxis_title="Month")
            st.plotly_chart(fig_trends, use_container_width=True)

            # Estimate Zero-Click Impact (using relative interest as a proxy)
            avg_interest = trends_df["Search Interest"].mean()
            zero_click_impact = avg_interest * 0.4  # 40% zero-click assumption
            st.write(f"**Estimated Zero-Click Impact**: If 40% of searches for '{selected_term}' are zero-click, approximately {int(zero_click_impact):.0f}% of relative search interest may not result in website clicks.")
        else:
            st.warning(f"No Google Trends data found for '{selected_term}'. Try another term or check spelling.")
    except Exception as e:
        st.error(f"Error fetching Google Trends data: {e}")
elif selected_term:
    st.error("Google Trends integration unavailable. Please check your connection or try again later.")

# Fallback: Visualize Local Dataset
st.subheader("Local Dataset Search Volume")
search_terms = df_search["Search Term"].unique().tolist()
selected_local_term = st.selectbox("Select a search term from local dataset", options=[""] + search_terms, index=0)

if selected_local_term:
    filtered_df = df_search[df_search["Search Term"].str.lower() == selected_local_term.lower()]
    
    if not filtered_df.empty:
        fig_search = px.line(
            filtered_df,
            x="Month",
            y="Search Volume",
            title=f"Monthly Search Volume for '{selected_local_term}' (Local Data)",
            labels={"Search Volume": "Search Volume"},
            markers=True
        )
        fig_search.update_layout(yaxis_title="Search Volume", xaxis_title="Month")
        st.plotly_chart(fig_search, use_container_width=True)

        # Highlight Zero-Click Impact
        zero_click_impact = filtered_df["Search Volume"] * 0.4
        st.write(f"**Estimated Zero-Click Impact**: If 40% of searches for '{selected_local_term}' are zero-click, approximately {int(zero_click_impact.mean()):,} searches per month may not result in website clicks.")
    else:
        st.warning(f"No local data found for '{selected_local_term}'. Please select another term.")

# File Uploader for Custom Dataset
st.subheader("Upload Your Own Search Volume Data")
uploaded_file = st.file_uploader("Upload a CSV file with columns: 'Search Term', 'Month', 'Search Volume'", type=["csv"])
if uploaded_file:
    df_uploaded = pd.read_csv(uploaded_file)
    if all(col in df_uploaded.columns for col in ["Search Term", "Month", "Search Volume"]):
        df_search = df_uploaded
        st.success("Dataset奢

# Additional Insights
st.subheader("What Are Zero-Click Searches?")
st.write("""
Zero-click searches occur when users find the information they need directly on the 
search engine results page (e.g., through featured snippets, knowledge panels, or maps). 
This trend highlights the growing importance of optimizing content for visibility 
directly on the SERP, as fewer users are clicking through to websites.
""")

# Interactive Slider
st.subheader("Explore the Impact")
click_through = st.slider(
    "Assume a website loses clicks due to zero-click searches. What % of traffic is lost?",
    min_value=0,
    max_value=100,
    value=40
)
st.write(f"If **{click_through}%** of searches are zero-click, a website could lose up to **{click_through}%** of its potential traffic from search results.")

# Footer
st.markdown("---")
st.write("Data source: Bain survey (2025), Google Trends, and sample data. Built with Streamlit.")
