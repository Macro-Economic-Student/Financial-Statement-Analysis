import streamlit as st

# Pages for percentage
single_feat_check_percentage = st.Page(
    "pages/percentage/single_feature_check_page_percentage.py", title="Single Feature Persentase", default=True
)
ovt_single_bank_check_percentage = st.Page(
    "pages/percentage/overtime_single_bank_check_page_percentage.py", title="Overtime Single Bank Persentase"
)
ovt_multiple_bank_check_percentage = st.Page(
    "pages/percentage/overtime_multiple_bank_check_page_percentage.py", title="Overtime Multiple Bank Persentase"
)

# Pages for number
single_feat_check_number = st.Page(
    "pages/number/single_feature_check_page_number.py", title="Single Feature Angka"
)
ovt_multiple_bank_check_number = st.Page(
    "pages/number/overtime_multiple_bank_check_page_number.py", title="Overtime Multiple Bank Angka"
)
ovt_single_bank_check_number = st.Page(
    "pages/number/overtime_single_bank_check_page_number.py", title="Overtime Single Bank Angka"
)

pg = st.navigation(
    {
        "Persentase" :[single_feat_check_percentage, ovt_multiple_bank_check_percentage, ovt_single_bank_check_percentage]
        # "Angka" :[single_feat_check_number, ovt_single_bank_check_number, ovt_multiple_bank_check_number]
    }
)

pg.run()