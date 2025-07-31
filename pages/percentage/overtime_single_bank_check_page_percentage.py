import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("# Overtime Single Bank Persentase")

with st.sidebar:
    st.markdown("## Overtime Single Bank Persentase")
    st.write(
        """
        📊 **Welcome to the Overtime Single Bank Visualization**
    
        This page provides **in-depth visualizations** of financial features **over time** for a selected **single bank**.

        📅 **Data Source:** Quarterly Financial Statements starting from **Q1 2023**

        ---

        🔍 **What you can explore:**
        - 🧾 Track individual financial indicators like **NPL**, **LDR**, **ROA**, and others **across time**
        - 📊 Compare **multiple financial features side-by-side** in one comprehensive chart
        - 🕵️‍♂️ Identify patterns, trends, and unusual movements over quarters

        ---

        📌 **Visualizations on this page:**
        - 📈 **Three line charts**: Each one shows a selected single feature’s performance over time for the selected bank
        - 🧩 **One comparison chart**: Overlay **three different features** in a single graph for easier comparison

        Use the dropdowns to customize the features shown, and click **Update** to refresh the graphs.

        """
    )

px.defaults.color_continuous_scale = "Viridis"
px.defaults.template = "plotly_white"  # or "ggplot2", "seaborn", etc.

# Convert year_quarter to a sortable key (e.g., 2024_q1 -> (2024, 1))
def quarter_sort_key(yq):
    year, q = yq.split('_q')
    return int(year) * 4 + int(q)

# File path for data
rasio_file_path = "data/summarized_rasio.xlsx"
df_rasio = pd.read_excel(rasio_file_path)
# Placeholder for combined df
df = df_rasio.copy()

# Sort company names in ascending order
sorted_companies = sorted(df['company_name'].unique())

# Set the category order explicitly
df['company_name'] = pd.Categorical(df['company_name'], categories=sorted_companies, ordered=True)

# Placeholder for list of company name
list_companies_to_check = sorted_companies

# Placeholder for list of features that can be checked
list_columns_to_check = [
    'npl_gross',
    'npl_net',
    'return_on_asset',
    'return_on_equity',
    'net_interest_margin'
]

for i in range(1, 4):
    st.header(f"📈 Line Chart {i}")

    date_key = f"date_range_selector_{i}"

    # Check if 'posisi' is already in datetime format, if not, convert it
    if not pd.api.types.is_datetime64_any_dtype(df['posisi']):
        df['posisi'] = pd.to_datetime(df['posisi'], errors='coerce')

    # Date filter
    min_date = df['posisi'].min()
    max_date = df['posisi'].max()

    with st.form(key=f"date_form_{i}"):
        start_date, end_date = st.date_input(
            f"Select date range for Chart {i+1}",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=date_key
        )
        submitted = st.form_submit_button("Apply Date Filter")

    col1, col2 = st.columns(2)
    with col1:
        company = st.selectbox(
            f"Select Company for Chart {i}",
            list_companies_to_check,
            index=list_companies_to_check.index(list_companies_to_check[i - 1]) if list_companies_to_check[i - 1] in list_companies_to_check else 0,
            key=f"company_select_{i}"
        )
    with col2:
        column = st.selectbox(
            f"Select Financial Feature for Chart {i}",
            list_columns_to_check,
            index=list_columns_to_check.index(list_columns_to_check[i - 1]) if list_columns_to_check[i - 1] in list_columns_to_check else 0,
            key=f"feature_select_{i}"
        )

    # Filter data
    df_filtered = df.copy()

    if submitted and start_date <= end_date:
        df_filtered = df_filtered[
            (df_filtered['posisi'].dt.date >= start_date) &
            (df_filtered['posisi'].dt.date <= end_date)
        ]

    # Filtered data based on company and date range
    df_filtered = df_filtered[
        (df_filtered["company_name"] == company) &
        (df_filtered["posisi"] >= pd.to_datetime(start_date)) &
        (df_filtered["posisi"] <= pd.to_datetime(end_date))
    ]
    df_filtered['sort_key'] = df_filtered['year_quarter'].apply(quarter_sort_key)
    df_filtered = df_filtered.sort_values(by='sort_key')

    # Plot
    fig = px.line(
        df_filtered,
        x='year_quarter',
        y=column,
        title=f"{column} Over Time ({company})",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Year Quarter",
        yaxis_title=column,
        xaxis=dict(categoryorder='array', categoryarray=df_filtered['year_quarter'])
    )
    fig.update_yaxes(tickformat=".02%")

    # ✅ Wrap each chart in its own container
    st.plotly_chart(fig, use_container_width=True, key=f"plotly_chart_{i}")


# Code for multiple columns, one company
# --- Section Header ---
st.header("📊 Multi-Line Chart for One Company")

# Date selection
# Check if 'posisi' is already in datetime format, if not, convert it
if not pd.api.types.is_datetime64_any_dtype(df['posisi']):
    df['posisi'] = pd.to_datetime(df['posisi'], errors='coerce')

# Date filter
min_date = df['posisi'].min()
max_date = df['posisi'].max()

with st.form(key=f"date_form_multi_feature"):
    start_date_multi, end_date_multi = st.date_input(
        f"Select date range :",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range_selector_multi_feature"
    )
    submitted = st.form_submit_button("Apply Date Filter")

# --- Selection ---
col1, col2 = st.columns(2)

with col1:
    company_multi = st.selectbox(
        "Select Company for Multi-Line Chart",
        list_companies_to_check,
        index=list_companies_to_check.index(list_companies_to_check[0]) if list_companies_to_check[0] in list_companies_to_check else 0,
        key="multi_company_select"
    )

with col2:
    columns_multi = st.multiselect(
        "Select Financial Features",
        options=list_columns_to_check,
        default=list_columns_to_check[:3],  # you can change this default list as needed
        key="multi_feature_select"
    )

# --- Filter & Sort ---
df_multi = df.copy()
if submitted and start_date_multi <= end_date_multi:
    df_multi = df_multi[
        (df_multi['posisi'].dt.date >= start_date_multi) &
        (df_multi['posisi'].dt.date <= end_date_multi)
    ]
# Filtered data based on company and date range
df_multi = df_multi[
    (df_multi["company_name"]== company_multi) &
    (df_multi["posisi"] >= pd.to_datetime(start_date_multi)) &
    (df_multi["posisi"] <= pd.to_datetime(end_date_multi))
]
df_multi['sort_key'] = df_multi['year_quarter'].apply(quarter_sort_key)
df_multi = df_multi.sort_values(by='sort_key')

# --- Plot ---
fig_multi = go.Figure()

for col in columns_multi:
    fig_multi.add_trace(
        go.Scatter(
            x=df_multi['year_quarter'],
            y=df_multi[col],
            mode='lines+markers',
            name=col
        )
    )

fig_multi.update_layout(
    title=f"Selected Features Over Time ({company_multi})",
    xaxis_title="Year Quarter",
    yaxis_title="Value",
    template="plotly_white",
    xaxis=dict(categoryorder='array', categoryarray=df_multi['year_quarter']),
    legend_title="Feature"
)
fig_multi.update_yaxes(tickformat=".02%")

# --- Show Plot ---
st.plotly_chart(fig_multi, use_container_width=True, key="multi_line_chart")

st.markdown("---")