import streamlit as st
import plotly.express as px
import pandas as pd

# Set page title and layout
st.set_page_config(page_title="Zero-Click & Search Trends Demo", layout="centered")

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

# Sample Dataset for Monthly Search Volumes
# Simulating a dataset with search terms and monthly volumes (e.g., from Google Keyword Planner or similar)
sample_data = {
    "Search Term": ["best laptops", "best laptops", "best laptops", "python tutorial", "python tutorial", "python tutorial", "cheap flights", "cheap flights", "cheap flights"],
    "Month": ["2025-01", "2025-02", "2025-03", "2025-01", "2025-02", "2025-03", "2025-01", "2025-02", "2025-03"],
    "Search Volume": [120000, 130000, 125000, 80000, 85000, 90000, 200000, 210000, 190000]
}
df_search = pd.DataFrame(sample_data)

# Save sample dataset to a CSV file for demonstration
df_search.to_csv("search_volume_data.csv", index=False)

# Load dataset (in practice, this could be a user-uploaded file)
try:
    df_search = pd.read_csv("search_volume_data.csv")
except FileNotFoundError:
    st.error("Search volume dataset not found. Using sample data.")
    df_search = pd.DataFrame(sample_data)

# Search Term Selection
st.subheader("Explore Monthly Search Volume Trends")
search_terms = df_search["Search Term"].unique().tolist()
selected_term = st.selectbox("Select or type a search term", options=[""] + search_terms, index=0)

# Allow user to input a custom search term
custom_term = st.text_input("Or enter a custom search term", "")

# Determine which term to use
if custom_term:
    selected_term = custom_term

# Visualize Search Volume
if selected_term:
    filtered_df = df_search[df_search["Search Term"].str.lower() == selected_term.lower()]
    
    if not filtered_df.empty:
        fig_search = px.line(
            filtered_df,
            x="Month",
            y="Search Volume",
            title=f"Monthly Search Volume for '{selected_term}'",
            labels={"Search Volume": "Search Volume"},
            markers=True
        )
        fig_search.update_layout(yaxis_title="Search Volume", xaxis_title="Month")
        st.plotly_chart(fig_search, use_container_width=True)

        # Highlight Zero-Click Impact
        zero_click_impact = filtered_df["Search Volume"] * 0.4  # Assuming 40% are zero-click
        st.write(f"**Estimated Zero-Click Impact**: If 40% of searches for '{selected_term}' are zero-click, approximately {int(zero_click_impact.mean()):,} searches per month may not result in website clicks.")
    else:
        st.warning(f"No data found for '{selected_term}'. Please select another term or ensure data is available.")
else:
    st.info("Select or enter a search term to view its monthly search volume trends.")

# Additional Insights
st.subheader("What Are Zero-Click Searches?")
st.write("""
Zero-click searches occur when users find the information they need directly on the 
search engine results page (e.g., through featured snippets, knowledge panels, or maps). 
This trend highlights the growing importance of optimizing content for visibility 
directly on the SERP, as fewer users are clicking through to websites.
""")

# Interactive Slider for Traffic Loss
st.subheader("Explore the Impact")
click_through = st.slider(
    "Assume a website loses clicks due to zero-click searches. What % of traffic is lost if 40% of searches are zero-click?",
    min_value=0,
    max_value=100,
    value=40
)
st.write(f"If **{click_through}%** of searches are zero-click, a website could lose up to **{click_through}%** of its potential traffic from search results.")

# File Uploader for Custom Dataset
st.subheader("Upload Your Own Search Volume Data")
uploaded_file = st.file_uploader("Upload a CSV file with columns: 'Search Term', 'Month', 'Search Volume'", type=["csv"])
if uploaded_file:
    df_uploaded = pd.read_csv(uploaded_file)
    if all(col in df_uploaded.columns for col in ["Search Term", "Month", "Search Volume"]):
        df_search = df_uploaded
        st.success("Dataset uploaded successfully! Select a search term to visualize.")
        search_terms = df_search["Search Term"].unique().tolist()
    else:
        st.error("Uploaded CSV must contain 'Search Term', 'Month', and 'Search Volume' columns.")

# Footer
st.markdown("---")
st.write("Data source: Bain survey (2025) and sample search volume data. Built with Streamlit.")
