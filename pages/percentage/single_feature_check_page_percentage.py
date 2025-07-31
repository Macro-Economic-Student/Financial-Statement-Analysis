import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("# Single Feature Persentase")

with st.sidebar:
    st.markdown("## Single Feature Persentase")
    st.write(
        """
        📊 **Welcome to the Single Feature Comparison**
    
        This page offers **visual comparisons of key financial indicators** across multiple companies in multiple quartiles.
    
        📅 Data Source: **Quarterly Financial Statements starting from Q1 2023**
    
        ---  
        
        🔍 **Explore company performance across features such as:**
        - 🧾 **Non-Performing Loan (NPL)**
        - 💰 **Loan-to-Deposit Ratio (LDR)**
        - 📈 **Return on Assets (ROA)**
        - 📊 And Many More
    
        ---
    
        🧪 **What you’ll see:**
        - 📦 **Boxplots**: Show the distribution, median, and outliers — giving insights into variability, risk, and relative standing among companies.
        - 📉 **Histograms**: Display the frequency distribution of each feature across all companies and quarters, helping spot concentration zones and anomalies.
    
        Use the dropdown to select specific financial features and click **Update** to refresh the visualizations.
    
        """
    )

px.defaults.color_continuous_scale = "Viridis"
px.defaults.template = "plotly_white"  # or "ggplot2", "seaborn", etc.

# File path for data
rasio_file_path = "data/summarized_rasio.xlsx"
df_rasio = pd.read_excel(rasio_file_path)
# Placeholder for combined df
df = df_rasio.copy()

# Get unique company names
# companies = df['company_name'].unique()

# Sort company names in ascending order
sorted_companies = sorted(df['company_name'].unique())

# Set the category order explicitly
df['company_name'] = pd.Categorical(df['company_name'], categories=sorted_companies, ordered=True)

# Placeholder for list of features that can be checked
list_columns_to_check = [
    'npl_gross',
    'npl_net',
    'return_on_asset',
    'return_on_equity',
    'net_interest_margin'
]

# --- Dropdown Selection ---
selected = st.selectbox(
    "Select a feature to visualize:",
    options=list_columns_to_check,
    index=list_columns_to_check.index(list_columns_to_check[0]) if list_columns_to_check[0] in list_columns_to_check else 0
)

# --- Use Current Selection for Visuals ---
column_to_check = selected

# --- Boxplot ---
fig_box = px.box(
    df,
    x=column_to_check,
    color='company_name',
    template="plotly_white",
    points='outliers',
    orientation='h',
    title=f'Boxplot of {column_to_check} by Company Name',
    category_orders={"company_name": sorted_companies}  # <-- Force the order
)
fig_box.update_xaxes(tickformat=".02%")
fig_box.update_layout(
    legend_title = "Company",
    shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="white", width=1),
            layer="below"
        )
    ]
)

# --- Histogram ---
# fig_hist = px.histogram(
#     df,
#     x=column_to_check,
#     color='company_name',
#     template="plotly_white",
#     nbins=20,
#     title=f'Histogram of {column_to_check} by company_name'
# )
# fig_hist.update_xaxes(tickformat=".02%")
# fig_hist.update_yaxes(title_text="Count of Observations")
# fig_hist.update_layout(
#     shapes=[
#         dict(
#             type="rect",
#             xref="paper", yref="paper",
#             x0=0, y0=0, x1=1, y1=1,
#             line=dict(color="white", width=1),
#             layer="below"
#         )
#     ]
# )

# Create Plotly stacked histogram
fig_go_hist = go.Figure()

for company in sorted_companies:
    fig_go_hist.add_trace(
        go.Histogram(
            x=df[df['company_name'] == company][column_to_check],
            name=company,
            opacity=0.75
        )
    )

fig_go_hist.update_layout(
    barmode='stack',
    template='plotly_white',
    title=f'Stacked Histogram of {column_to_check} by Company Name',
    xaxis_title=f'{column_to_check}',
    yaxis_title='Count of Observations',
    legend_title='Company'
)

# Add borders to bars
fig_go_hist.update_traces(marker_line_color="white", marker_line_width=1)
fig_go_hist.update_xaxes(tickformat=".02%")
fig_go_hist.update_layout(
    shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="white", width=1),
            layer="below"
        )
    ],
    legend_traceorder="normal"  # 🔥 keeps legend in trace (loop) order
)

# Compute statistics from the entire dataset
x_data = df[column_to_check]
mean_val = x_data.mean()
median_val = x_data.median()
q1 = x_data.quantile(0.25)
q3 = x_data.quantile(0.75)
# Compute percentiles
p5 = x_data.quantile(0.05)
p15 = x_data.quantile(0.15)
p85 = x_data.quantile(0.85)
p95 = x_data.quantile(0.95)

# Add vertical lines to the figure
for stat_val, label, color in zip(
    [mean_val, median_val, q1, q3],
    ["Mean", "Median", "Q1", "Q3"],
    ["red", "green", "blue", "purple"]
):
    fig_go_hist.add_vline(
        x=stat_val,
        line_width=2,
        line_dash="dash",
        line_color=color,
        annotation_text=label,
        annotation_position="top",
    )

# Create summary table
summary_stats = {
    'Statistic': [
        'Min', 'P5', 'P15', 'Q1', 
        'Mean', 'Median','Q3',
        'P85', 'P95', 'Max', 'Std Dev'
    ],
    column_to_check: [
        x_data.min(), p5, p15, q1,
        mean_val, median_val,  q3,
        p85, p95, x_data.max(), x_data.std()
    ]
}
summary_df = pd.DataFrame(summary_stats)

# --- Display ---
st.subheader(f"Boxplot of {column_to_check}")
st.plotly_chart(fig_box, use_container_width=True)

# st.subheader(f"Histogram of {column_to_check}")
# st.plotly_chart(fig_hist, use_container_width=True)

st.subheader(f"Histogram of {column_to_check}")
st.plotly_chart(fig_go_hist, use_container_width=True)

# Show table in Streamlit
st.markdown("### Statistical Summary")
st.dataframe(summary_df.style.format({column_to_check: "{:.4f}"}))