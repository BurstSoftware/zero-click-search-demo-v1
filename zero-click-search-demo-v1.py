import streamlit as st
import plotly.express as px
import pandas as pd

# Set page title and layout
st.set_page_config(page_title="Zero-Click Search Demo", layout="centered")

# Title
st.title("Zero-Click Search Results: A Growing Trend")

# Explanation
st.write("""
According to a recent Bain survey, **80% of consumers** rely on **zero-click results** 
in at least **40% of their searches**. This means they get their answers directly 
on the search engine results page (SERP) without clicking through to a website.
""")

# Data for visualization
data = {
    "Category": ["Consumers Using Zero-Click", "Searches with Zero-Click"],
    "Percentage": [80, 40]
}
df = pd.DataFrame(data)

# Create bar chart
fig = px.bar(
    df,
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
fig.update_traces(texttemplate="%{text}%", textposition="auto")
fig.update_layout(showlegend=False, yaxis_range=[0, 100])

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Additional insights
st.subheader("What Are Zero-Click Searches?")
st.write("""
Zero-click searches occur when users find the information they need directly on the 
search engine results page (e.g., through featured snippets, knowledge panels, or maps). 
This trend highlights the growing importance of optimizing content for visibility 
directly on the SERP, as fewer users are clicking through to websites.
""")

# Interactive element
st.subheader("Explore the Impact")
click_through = st.slider(
    "Assume a website loses clicks due to zero-click searches. What % of traffic is lost if 40% of searches are zero-click?",
    min_value=0,
    max_value=100,
    value=40
)
st.write(f"If **{click_through}%** of searches are zero-click, a website could lose up to **{click_through}%** of its potential traffic from search results.")

# Footer
st.markdown("---")
st.write("Data source: Bain survey (2025). Built with Streamlit.")
