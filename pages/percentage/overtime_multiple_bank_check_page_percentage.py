import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("# Overtime Multiple Bank Persentase")

with st.sidebar:
    st.markdown("## Overtime Multiple Bank Persentase")
    st.write(
        """
        📊 **Welcome to the Overtime Multiple Bank Visualization**
    
        This page provides **comparative visualizations** of selected financial indicators across **multiple banks** over time.

        📅 **Data Source:** Quarterly Financial Statements starting from **Q1 2023**

        ---

        🔍 **What you can explore:**
        - 📈 Track how a **single financial indicator** (e.g., ROA, LDR, NIM) evolves across time for **several banks**
        - 🏦 Compare multiple banks side-by-side in terms of their **performance trends**
        - 🕵️‍♂️ Spot outliers, convergence patterns, or sudden shifts among peers

        ---

        📌 **Visualizations on this page:**
        - 🔁 **Three multi-line charts**: Each one allows you to choose a feature (e.g., ROA) and visualize it for several selected companies across time
        - ⚙️ Fully interactive controls: Select different features and banks for each chart independently

        Use the dropdowns to customize your analysis. Each chart updates individually, so you can explore multiple comparisons at once.
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

# Ensure quarter sorting is applied
df['sort_key'] = df['year_quarter'].apply(quarter_sort_key)
df = df.sort_values(by='sort_key')

# Default values
default_feature = "ROA" if "ROA" in list_columns_to_check else list_columns_to_check[0]
default_companies = list_companies_to_check[:2]

# Helper function to render one chart block
def render_multi_company_chart(index: int):
    st.markdown(f"#### 📊 Chart {index+1}: Compare Companies on One Feature")

    col_key = f"feature_selector_{index}"
    company_key = f"company_selector_{index}"
    date_key = f"date_range_selector_{index}"
    chart_key = f"plotly_chart_{index}"
    df_key = f"plotly_df_{index}"

    # Check if 'posisi' is already in datetime format, if not, convert it
    if not pd.api.types.is_datetime64_any_dtype(df['posisi']):
        df['posisi'] = pd.to_datetime(df['posisi'], errors='coerce')

    # Date filter
    min_date = df['posisi'].min()
    max_date = df['posisi'].max()

    start_date, end_date = st.date_input(
        f"Select date range for Chart {index+1}",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=date_key
    )

    # Selectors
    column_to_check = st.selectbox(
        f"Select feature for Chart {index+1}",
        options=list_columns_to_check,
        index=list(list_columns_to_check).index(default_feature),
        key=col_key
    )

    selected_companies = st.multiselect(
        f"Select companies for Chart {index+1}",
        options=list_companies_to_check,
        default=default_companies,
        key=company_key
    )

    # Filtered data based on company and date range
    df_filtered = df[
        (df["company_name"].isin(selected_companies)) &
        (df["posisi"] >= pd.to_datetime(start_date)) &
        (df["posisi"] <= pd.to_datetime(end_date))
    ]

    # Plot
    fig = px.line(
        df_filtered,
        x='year_quarter',
        y=column_to_check,
        color='company_name',
        markers=True,
        title=f"{column_to_check} Over Time (Chart {index+1})"
    )

    # Compute summary stats from filtered data
    values = df_filtered[column_to_check].dropna()

    stats = {
        "Min": values.min(),
        "P5": np.percentile(values, 5),
        "P15": np.percentile(values, 15),
        "Q1 (25%)": values.quantile(0.25),
        "Mean": values.mean(),
        "Median": values.median(),
        "Q3 (75%)": values.quantile(0.75),
        "P85": np.percentile(values, 85),
        "P95": np.percentile(values, 95),
        "Max": values.max(),
        "Std": values.std()
    }

    # Add horizontal lines for key stats
    highlight_stats = {
        "Mean": ("white", stats["Mean"]),
        "Median": ("firebrick", stats["Median"]),
        "Q1 (25%)": ("royalblue", stats["Q1 (25%)"]),
        "Q3 (75%)": ("green", stats["Q3 (75%)"]),
    }

    for label, (color, y_val) in highlight_stats.items():
        fig.add_trace(
            go.Scatter(
                x=[df_filtered['year_quarter'].min(), df_filtered['year_quarter'].max()],
                y=[y_val, y_val],
                mode="lines",
                line=dict(color=color, dash="dash"),
                name=label,
                hovertemplate=f"{label}: {y_val:.2%}<extra></extra>",
                showlegend=True
            )
        )

    # Lock x-axis order
    fig.update_layout(
        xaxis_title="Year Quarter",
        yaxis_title=column_to_check,
        xaxis=dict(categoryorder='array', categoryarray=df_filtered['year_quarter'].unique()),
        yaxis=dict(tickformat=".2%"),
        legend_traceorder="normal",
        template="plotly_white"
    )

    # Layout the chart and the stats side by side
    col1, col2 = st.columns([3, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True, key=chart_key)

    with col2:
        summary_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
        summary_df = summary_df.loc[[
            "Min", "P5", "P15", "Q1 (25%)", "Mean", "Median",
            "Q3 (75%)", "P85", "P95", "Max", "Std"
        ]]
        summary_df = summary_df.applymap(lambda x: f"{x:.2%}")
        st.dataframe(summary_df, use_container_width=True, key=df_key)

# --- Render all three charts ---
st.markdown("## 📈 Multi-Line Comparisons: Company vs Feature Over Time")
for i in range(3):
    render_multi_company_chart(i)
    st.markdown("---")