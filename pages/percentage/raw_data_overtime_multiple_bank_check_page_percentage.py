import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
# import operator
from io import BytesIO
from openpyxl import Workbook

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

st.markdown(f"#### 📊 Chart: Raw Data for Comparing Companies on One Feature")

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
        f"Select date range for Chart",
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
        f"Select feature for Chart",
        options=item_dict_list,
        index=item_dict_list.index(default_display),
        key=col_key
    )
    # Convert back to original column key
    column_to_check = reverse_map[selected_display]
    
with col2 :
    selected_kbmi = st.multiselect(
        f"Select KBMI for Chart",
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
    f"Select companies for Chart",
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
        f"Select year for Chart",
        options=valid_years,
        default=valid_years,
        key=year_key
    )
with col4 :
    selected_quartile = st.multiselect(
        f"Select quartile for Chart",
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


# Create column order (sorted by year ascending, quarter order Q1..Q4)
quarter_order = ['q1', 'q2', 'q3', 'q4']

# build a sorted list of (year, quarter) present
unique_yq = df_filtered[['year', 'quarter']].drop_duplicates()
unique_yq['q_order'] = unique_yq['quarter'].apply(lambda q: quarter_order.index(q) if q in quarter_order else 99)
unique_yq = unique_yq.sort_values(['year', 'q_order'])
col_tuples = [(int(r['year']), r['quarter']) for _, r in unique_yq.iterrows()]

# pivot (agg mean in case of multiple rows per company-quarter)
pivot = df_filtered.pivot_table(index='company_name',
                           columns=['year', 'quarter'],
                           values=column_to_check,
                           aggfunc='mean')

# Reindex columns to ensure sorted order and present all col_tuples
# Build MultiIndex in desired order
ordered_cols = pd.MultiIndex.from_tuples(col_tuples, names=['year', 'quarter'])
# Reindex to include missing columns as NaN if needed
pivot = pivot.reindex(columns=ordered_cols, fill_value=np.nan)

# ---------- Column-wise summary (bottom row) ----------
col_stats = {}
series_all = pivot  # DataFrame: rows companies, cols multiindex
for col in pivot.columns:
    s = pivot[col].dropna()
    if s.empty:
        col_stats[col] = {k: np.nan for k in ["Min","P5","P15","Q1","Mean","Median","Q3","P85","P95","Max","Std"]}
        continue
    arr = s.values
    col_stats[col] = {
        "Min": np.nanmin(arr),
        "P5": np.nanpercentile(arr, 5),
        "P15": np.nanpercentile(arr, 15),
        "Q1": np.nanpercentile(arr, 25),
        "Mean": np.nanmean(arr),
        "Median": np.nanmedian(arr),
        "Q3": np.nanpercentile(arr, 75),
        "P85": np.nanpercentile(arr, 85),
        "P95": np.nanpercentile(arr, 95),
        "Max": np.nanmax(arr),
        "Std": np.nanstd(arr, ddof=0)
    }

# Build bottom summary DataFrame with same MultiIndex columns
bottom_df = pd.DataFrame({col: pd.Series(col_stats[col]) for col in pivot.columns})
# bottom_df index = statistic keys; columns = MultiIndex
# We'll transpose later for display if needed.

# ---------- Row-wise summary (right side) ----------
row_stats = []
for idx, row in pivot.iterrows():
    vals = row.dropna().values
    if vals.size == 0:
        stats_row = {k: np.nan for k in ["Min","P5","P15","Q1","Mean","Median","Q3","P85","P95","Max","Std"]}
    else:
        stats_row = {
            "Min": np.nanmin(vals),
            "P5": np.nanpercentile(vals, 5),
            "P15": np.nanpercentile(vals, 15),
            "Q1": np.nanpercentile(vals, 25),
            "Mean": np.nanmean(vals),
            "Median": np.nanmedian(vals),
            "Q3": np.nanpercentile(vals, 75),
            "P85": np.nanpercentile(vals, 85),
            "P95": np.nanpercentile(vals, 95),
            "Max": np.nanmax(vals),
            "Std": np.nanstd(vals, ddof=0)
        }
    row_stats.append((idx, stats_row))

row_stats_df = pd.DataFrame([s for _, s in row_stats], index=[r for r, _ in row_stats])
# reorder columns
row_stats_df = row_stats_df[["Min","P5","P15","Q1","Mean","Median","Q3","P85","P95","Max","Std"]]

# ---------- Formatting functions ----------
def needs_percent_format(series: pd.Series) -> bool:
    """Heuristic: return True if values look like proportions (-1..1)"""
    if series.dropna().empty:
        return False
    smin = series.min()
    smax = series.max()
    return (smin >= -1.0 and smax <= 1.0)

def fmt_value(x, percent_mode: bool):
    if pd.isna(x):
        return ""
    try:
        if percent_mode:
            return f"{x:.2%}"
        # else numeric with thousands separators (or float 4 decimals)
        if float(x).is_integer():
            return f"{int(x):,}"
        return f"{x:,.4f}"
    except Exception:
        return str(x)

# ---------- Formatting decision ----------
# percent_mode = needs_percent_format(pivot.stack(dropna=True) if not pivot.empty else pd.Series(dtype=float))

# Format pivot for display: create display strings but keep numeric copies for downloads if desired
percent_mode = True  # force percent mode for this page
display_pivot = pivot.copy().astype(float)
display_pivot = display_pivot.applymap(lambda x: fmt_value(x, percent_mode))

# Create bottom summary display (as a single-row DataFrame matching pivot columns)
display_bottom = bottom_df.applymap(lambda x: fmt_value(x, percent_mode))

# Create row summary display
display_row_stats = row_stats_df.applymap(lambda x: fmt_value(x, percent_mode))

# ---------- Combine table for visual output ----------
# Streamlit can render MultiIndex columns; we'll show pivot (companies x year/quarter) with bottom row visually
st.markdown("### Raw table (rows = companies, columns = Year → Quarter)")

# Use two-column layout: left wide for table, right narrow for row-summary
left_col, right_col = st.columns([4, 1.2])

with left_col:
    st.markdown("#### Table")
    # Show table
    # We'll display pivot with MultiIndex columns (string values). To show bottom summary, we can show bottom separately
    st.dataframe(display_pivot, use_container_width=True, key="raw_table_pivot")

    st.markdown("#### Column-wise summary (bottom)")
    # bottom_df has index stats x columns (multiindex). We want to present as table where columns = same as pivot
    # transposed for readability
    bottom_t = display_bottom.T
    bottom_t.index = pd.MultiIndex.from_tuples(bottom_t.index)  # ensure MultiIndex names preserved
    st.dataframe(bottom_t, use_container_width=True, key="raw_table_bottom")

with right_col:
    st.markdown("#### Row summary (per company)")
    st.dataframe(display_row_stats, use_container_width=True, key="raw_table_row_summary")

# ---------- Optional download buttons ----------
@st.cache_data
def to_csv_bytes(df_obj):
    return df_obj.to_csv(index=True).encode('utf-8')

st.download_button("Download pivot CSV", data=to_csv_bytes(pivot), file_name=f"pivot_{selected_display}.csv", mime="text/csv")
st.download_button("Download row-summary CSV", data=to_csv_bytes(row_stats_df), file_name=f"row_summary_{selected_display}.csv", mime="text/csv")

def df_to_excel_bytes(df_dict: dict):
    """
    df_dict: {"sheet_name": dataframe}
    returns binary XLSX file in memory
    Uses pandas.ExcelWriter (openpyxl engine) so MultiIndex is handled correctly.
    """
    output = BytesIO()
    # use pandas ExcelWriter which will properly write MultiIndex columns/index
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in df_dict.items():
            # sanitize sheet name length
            safe_name = str(sheet_name)[:31]
            # If df has MultiIndex columns or index, to_excel will write them correctly
            # Write DataFrame 'df' to the sheet
            df.to_excel(writer, sheet_name=safe_name, index=True)
        writer.save()
    return output.getvalue()

# Prepare full export
excel_file = df_to_excel_bytes({
    "Pivot Table": pivot,                    # numeric pivot (MultiIndex cols)
    "Row Summary": row_stats_df,             # numeric summary per row
    "Display Pivot": display_pivot,          # formatted strings (if you want a pretty sheet)
    "Display Row Summary": display_row_stats # formatted strings
})

st.download_button(
    "📥 Download as Excel (.xlsx)",
    data=excel_file,
    file_name=f"raw_data_{selected_display}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)