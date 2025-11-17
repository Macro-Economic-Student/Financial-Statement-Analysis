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

st.markdown("# Raw Data Overtime Multiple Bank Persentase")

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

