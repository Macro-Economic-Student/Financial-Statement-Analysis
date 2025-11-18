import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
import operator

# add "../data" to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2] / "data"))

from import_data import import_rasio, import_fitur_rasio, import_dictionary_rasio

st.set_page_config(layout="wide")

st.markdown("# Raw Data Overtime Multiple Bank Persentase")

with st.sidebar:
    st.markdown("## Overtime Multiple Bank Persentase")
    st.write(
        """
        📊 **Welcome to the Overtime Multiple Bank Visualization**
    
        This page provides **comparative visualizations** of selected financial indicators across **multiple banks** over time.

        📅 **Data Source:** Quarterly Financial Statements starting from **Q1 2020**

        ---

        🔍 **What you can explore:**
        - 📈 Track how a **single financial indicator** (e.g., ROA, LDR, NIM) evolves across time for **several banks**
        - 🏦 Compare multiple banks side-by-side in terms of their **performance trends**
        - 🕵️‍♂️ Spot outliers, convergence patterns, or sudden shifts among peers

        ---

        📌 **Visualizations on this page:**
        - 🔁 **Detail Table for Data**: Table allows you to choose a feature (e.g., ROA) and visualize it for several selected companies across time
        - ⚙️ Fully interactive controls: Select different features and banks to customize your analysis


        """
    )

px.defaults.color_continuous_scale = "Viridis"
px.defaults.template = "plotly_white"  # or "ggplot2", "seaborn", etc.

# Convert year_quarter to a sortable key (e.g., 2024_q1 -> (2024, 1))
def quarter_sort_key(yq):
    year, q = yq.split('_q')
    return int(year) * 4 + int(q)

# File path for data
# rasio_file_path = "data/summarized_rasio.xlsx"
# df_rasio = pd.read_excel(rasio_file_path)
df_rasio = import_rasio()

df = df_rasio.copy()

# Sort company names in ascending order
sorted_companies = sorted(df['company_name'].unique())

# Sort year in ascending order
sorted_year = sorted(df['year'].unique())

# Sort quartile in ascending order
sorted_quartile = sorted(df['quarter'].unique())

# Sort kbmi type in ascending order
sorted_kbmi = sorted(df['kbmi_type'].unique())

# Set the category order explicitly
df['company_name'] = pd.Categorical(df['company_name'], categories=sorted_companies, ordered=True)

# Placeholder for list of company name
list_companies_to_check = sorted_companies

# Placeholder for list of features that can be checked
list_columns_to_check = import_fitur_rasio()

# Placeholder for dictionary of features that can be checked
dict_rasio = import_dictionary_rasio()
# Build the display list from dictionary values
item_dict_list = [dict_rasio[item] for item in list_columns_to_check]
# Map back from display value -> original key
reverse_map = {dict_rasio[item]: item for item in list_columns_to_check}

# Ensure quarter sorting is applied
df['sort_key'] = df['year_quarter'].apply(quarter_sort_key)
df = df.sort_values(by='sort_key')

# Default values
default_feature = "ROA" if "ROA" in list_columns_to_check else list_columns_to_check[0]
default_display = dict_rasio[default_feature]
default_companies = list_companies_to_check[:2]
default_year = sorted_year
default_quartile = sorted_quartile
default_kbmi = sorted_kbmi

index = 0

st.markdown(f"#### 📊 Chart {index+1}: Raw Data for Comparing Companies on One Feature")

col_key = f"feature_selector_{index}"
company_key = f"company_selector_{index}"
date_key = f"date_range_selector_{index}"
date_form_key = f"date_form_{index}"
year_key = f"year_selector_{index}"
quartile_key = f"quartile_selector_{index}"
kbmi_key = f"kbmi_selector_{index}"
chart_key = f"plotly_chart_{index}"
df_key = f"plotly_df_{index}"
rule_form_key = f"rule_form_{index}"
sign_selectbox_key = f"sign_selectbox_{index}"
percent_number_input_key = f"percent_number_input_{index}"
df_form_key = f"plotly_df_form_{index}"


# Check if 'posisi' is already in datetime format, if not, convert it
if not pd.api.types.is_datetime64_any_dtype(df['posisi']):
    df['posisi'] = pd.to_datetime(df['posisi'], errors='coerce')

# Date filter
min_date = df['posisi'].min()
max_date = df['posisi'].max()

# df_filtered for dataframe that will be changed
df_filtered = df.copy()

with st.form(key=date_form_key):
    start_date, end_date = st.date_input(
        f"Select date range for Chart {index+1}",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=date_key
    )
    submitted = st.form_submit_button("Apply Date Filter")

# Selectors
col1, col2 = st.columns(2)
with col1 :
    selected_display = st.selectbox(
        f"Select feature for Chart {index+1}",
        options=item_dict_list,
        index=item_dict_list.index(default_display),
        key=col_key
    )
    # Convert back to original column key
    column_to_check = reverse_map[selected_display]
    
with col2 :
    selected_kbmi = st.multiselect(
        f"Select KBMI for Chart {index+1}",
        options=sorted_kbmi,
        default=default_kbmi,
        key=kbmi_key
    )
    
if selected_kbmi:
    valid_companies = (
        df.loc[df["kbmi_type"].isin(selected_kbmi), "company_name"]
        .dropna().drop_duplicates().sort_values().tolist()
    )
else:
    # if no KBMI selected, allow all companies (or set to [] if you prefer)
    valid_companies = sorted(df["company_name"].dropna().unique().tolist())

selected_companies = st.multiselect(
    f"Select companies for Chart {index+1}",
    options=valid_companies,
    default=valid_companies,
    key=company_key
)

# Add mask for filtered dataframe
mask_posisi = ((df_filtered['posisi'].dt.date >= start_date) &
        (df_filtered['posisi'].dt.date <= end_date)) if (submitted and start_date <= end_date) else True
mask_kbmi_type = df_filtered["kbmi_type"].isin(selected_kbmi) if selected_kbmi else True
mask_company_name = df_filtered["company_name"].isin(selected_companies) if selected_companies else True


# normalize year to numeric for sorting
years_series = pd.to_numeric(df.loc[mask_kbmi_type & mask_company_name, "year"], errors="coerce")
valid_years = sorted(years_series.dropna().astype(int).unique().tolist())

col3, col4 = st.columns(2)

with col3 :
    selected_year = st.multiselect(
        f"Select year for Chart {index+1}",
        options=valid_years,
        default=valid_years,
        key=year_key
    )
with col4 :
    selected_quartile = st.multiselect(
        f"Select quartile for Chart {index+1}",
        options=sorted_quartile,
        default=default_quartile,
        key=quartile_key
    )

mask_year = df_filtered["year"].isin(selected_year) if selected_year else True
mask_quarter = df_filtered["quarter"].isin(selected_quartile) if selected_quartile else True

# Filtered data based on company and date range
df_filtered = df_filtered[
    mask_posisi & mask_kbmi_type & mask_company_name & mask_year & mask_quarter
]