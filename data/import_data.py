import pandas as pd
from pathlib import Path

def merge_two_df(df1: pd.DataFrame, df2: pd.DataFrame, on: list, exclude_cols: list) -> pd.DataFrame:
    # Combining df with df_kpmm_4
    df = pd.merge(
        df1,
        df2,
        on=on,
        how='left',
        suffixes=("", "_df2")
    )

    # drop only the df2 versions of excluded columns
    drop_cols = [f"{c}_df2" for c in exclude_cols if f"{c}_df2" in df.columns]
    df = df.drop(columns=drop_cols, errors="ignore")

    return df

def import_rasio() -> pd.DataFrame:
    """
    Import all Rasio data into one dataframe
    """

    exclude_cols = [
        'posisi',
        'company_name',
        'kbmi_type',
        'year',
        'quarter',
        'year_quarter',
        'company_date',
    ]
    
    # Path to this file's folder ("data")
    base_path = Path(__file__).parent

    # Build absolute paths to the Excel files (KBMI 4)
    file1 = base_path / "summarized rasio - KBMI 1.xlsx"
    file4 = base_path / "summarized rasio - KBMI 4.xlsx"
    file_aset_4 = base_path / "summarized fitur aset - KBMI 4.xlsx"
    file_liabilitas_4 = base_path / "summarized fitur liabilitas - KBMI 4.xlsx"
    file_kpmm_4 = base_path / "summarized fitur kpmm - KBMI 4.xlsx"
    file_kualitas_4 = base_path / "summarized fitur Kualitas Aset - KBMI 4.xlsx"
    file_laba_rugi_4 = base_path / "summarized fitur Laba Rugi - KBMI 4.xlsx"
    file_lcr_nsfr_4 = base_path / "summarized fitur lcr nsfr - KBMI 4.xlsx"

    # Build absolute paths to the Excel files (KBMI 2)
    file2 = base_path / "summarized rasio - KBMI 2.xlsx"
    file_aset_2 = base_path / "summarized fitur aset - KBMI 2.xlsx"
    file_liabilitas_2 = base_path / "summarized fitur liabilitas - KBMI 2.xlsx"
    file_kpmm_2 = base_path / "summarized fitur kpmm - KBMI 2.xlsx"
    file_kualitas_2 = base_path / "summarized fitur Kualitas Aset - KBMI 2.xlsx"
    file_laba_rugi_2 = base_path / "summarized fitur Laba Rugi - KBMI 2.xlsx"
    file_lcr_nsfr_2 = base_path / "summarized fitur lcr nsfr - KBMI 2.xlsx"

    # Build absolute paths to the Excel files (KBMI 3)
    file3 = base_path / "summarized rasio - KBMI 3.xlsx"
    file_aset_3 = base_path / "summarized fitur aset - KBMI 3.xlsx"
    file_liabilitas_3 = base_path / "summarized fitur liabilitas - KBMI 3.xlsx"
    file_kpmm_3 = base_path / "summarized fitur kpmm - KBMI 3.xlsx"
    file_kualitas_3 = base_path / "summarized fitur Kualitas Aset - KBMI 3.xlsx"
    file_laba_rugi_3 = base_path / "summarized fitur Laba Rugi - KBMI 3.xlsx"
    file_lcr_nsfr_3 = base_path / "summarized fitur lcr nsfr - KBMI 3.xlsx"

    # Read all data files
    df_kbmi_1 = pd.read_excel(file1)
    df_kbmi_1 = df_kbmi_1.drop(columns=["sort_key"], errors="ignore")

    # Read KBMI 4 files
    df_kbmi_4 = pd.read_excel(file4)
    df_aset_4 = pd.read_excel(file_aset_4)
    df_liabilitas_4 = pd.read_excel(file_liabilitas_4)
    df_kpmm_4 = pd.read_excel(file_kpmm_4)
    df_kualitas_4 = pd.read_excel(file_kualitas_4)
    df_laba_rugi_4 = pd.read_excel(file_laba_rugi_4)
    df_lcr_nsfr_4 = pd.read_excel(file_lcr_nsfr_4)

     # Read KBMI 2 files
    df_kbmi_2 = pd.read_excel(file2)
    df_aset_2 = pd.read_excel(file_aset_2)
    df_liabilitas_2 = pd.read_excel(file_liabilitas_2)
    df_kpmm_2 = pd.read_excel(file_kpmm_2)
    df_kualitas_2 = pd.read_excel(file_kualitas_2)
    df_laba_rugi_2 = pd.read_excel(file_laba_rugi_2)
    # df_lcr_nsfr_2 = pd.read_excel(file_lcr_nsfr_2)

     # Read KBMI 3 files
    df_kbmi_3 = pd.read_excel(file3)
    df_aset_3 = pd.read_excel(file_aset_3)
    df_liabilitas_3 = pd.read_excel(file_liabilitas_3)
    df_kpmm_3 = pd.read_excel(file_kpmm_3)
    df_kualitas_3 = pd.read_excel(file_kualitas_3)
    df_laba_rugi_3 = pd.read_excel(file_laba_rugi_3)
    # df_lcr_nsfr_3 = pd.read_excel(file_lcr_nsfr_3)

    # Combining df rasio KBMI 1 and KBMI 4
    df = pd.concat([df_kbmi_1, df_kbmi_4], axis=0, join="outer", ignore_index=True)

    # Combining df with df_aset_4
    df = merge_two_df(df, df_aset_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_liabilitas_4
    df = merge_two_df(df, df_liabilitas_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kpmm_4
    df = merge_two_df(df, df_kpmm_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kualitas_4
    df = merge_two_df(df, df_kualitas_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_laba_rugi_4
    df = merge_two_df(df, df_laba_rugi_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_laba_rugi_4
    df = merge_two_df(df, df_lcr_nsfr_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining with KBMI 2 data
    df_all_2 = df_kbmi_2.copy()
    # Combining df with df_aset_2
    df_all_2 = merge_two_df(df_all_2, df_aset_2, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_liabilitas_2
    df_all_2 = merge_two_df(df_all_2, df_liabilitas_2, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kpmm_2
    df_all_2 = merge_two_df(df_all_2, df_kpmm_2, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kualitas_2
    df_all_2 = merge_two_df(df_all_2, df_kualitas_2, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_laba_rugi_2
    df_all_2 = merge_two_df(df_all_2, df_laba_rugi_2, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining with KBMI 3 data
    df_all_3 = df_kbmi_3.copy()
    # Combining df with df_aset_3
    df_all_3 = merge_two_df(df_all_3, df_aset_3, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_liabilitas_3
    df_all_3 = merge_two_df(df_all_3, df_liabilitas_3, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kpmm_3
    dfdf_all_3 = merge_two_df(df_all_3, df_kpmm_3, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_kualitas_3
    df_all_3 = merge_two_df(df_all_3, df_kualitas_3, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    # Combining df with df_laba_rugi_3
    df_all_3 = merge_two_df(df_all_3, df_laba_rugi_3, on=['posisi', 'company_name'], exclude_cols=exclude_cols)


    df_combined_kbmi_2_3_4 = pd.concat([df, df_all_2, df_all_3], axis=0, join="outer", ignore_index=True)
    return df_combined_kbmi_2_3_4

def import_fitur_rasio() -> list :
    fitur_rasio = [
        'aset_produktif_bermasalah_dan_aset_non_produktif_bermasalah_terhadap_total_aset_produktif_dan_aset_non_produktif',
        'cadangan_kerugian_penurunan_nilai_(ckpn)_aset_keuangan_terhadap_aset_produktif',
        'npl_gross',
        'npl_net',
        'return_on_asset',
        'return_on_equity',
        'net_interest_margin',
        'biaya_operasional_terhadap_pendapatan_operasional',
        'loan_to_deposit_ratio',
        'posisi_devisa_neto_(pdn)_secara_keseluruhan',

        # Fitur dari Aset
        'penempat_pada_bank_lain_per_total_aset',
        'tagihan_spot_derivatif_forward_per_total_aset',
        'surat_berharga_yang_dimiliki_per_total_aset',
        'reverse_repo_per_total_aset',
        'tagihan_akseptasi_per_total_aset',
        'kyd_dan_pembiayaan_syariah_per_total_aset',
        'ckpn_aset_keuangan_per_kyd_dan_pembiayaan_syariah',

        # Fitur dari Liabilitas
        'casa_ratio',
        'rim_ratio',

        # Fitur dari Modal
        'kpmm_per_car',
        'kpmm_cet1',
        'modal_terhadap_aset',
        'modal_terhadap_kredit_bersih',
        'other_comprehensive_income_to_equity',

        # Fitur dari Kualitas Aset
        'ckpn_per_kredit_restruk',
        'ckpn_stage_2_3_per_kredit_restruk',
        'kredit_bermasalah_dan_restruk_per_kredit_yang_diberikan',
        'kredit_restruk_per_modal_inti',
        'laba_per_kredit_bermasalah_non_restruk',
        'laba_per_kredit_restruk',
        'total_npl_dan_restruk_npl_per_kredit_yang_diberikan',

        # Fitur dari Laba Rugi
        # 'other_comprehensive_income',
        'kredit_restruk_per_pendapatan_bunga',

        # Fitur dari LCR dan NSFR
        'lcr',
        'nsfr',
    ]

    return(fitur_rasio)

def import_dictionary_rasio() -> dict :
    dict_rasio = {
        'aset_produktif_bermasalah_dan_aset_non_produktif_bermasalah_terhadap_total_aset_produktif_dan_aset_non_produktif': 'Aset Bermasalah per Total Aset',
        'cadangan_kerugian_penurunan_nilai_(ckpn)_aset_keuangan_terhadap_aset_produktif': 'CKPN per Aset Prod',
        'npl_gross': 'NPL Gross',
        'npl_net': 'NPL Net',
        'return_on_asset': 'ROA',
        'return_on_equity': 'ROE',
        'net_interest_margin': 'NIM',
        'biaya_operasional_terhadap_pendapatan_operasional': 'BOPO',
        'loan_to_deposit_ratio': 'LDR',
        'posisi_devisa_neto_(pdn)_secara_keseluruhan': 'PDN',

        # Fitur dari Aset
        'penempat_pada_bank_lain_per_total_aset' : 'Penempatan pada Bank Lain per Total Aset',
        'tagihan_spot_derivatif_forward_per_total_aset' : 'Tagihan Spot Derivatif Forward per Total Aset',
        'surat_berharga_yang_dimiliki_per_total_aset' : 'Surat Berharga yang Dimiliki per Total Aset',
        'reverse_repo_per_total_aset' : 'Reverse Repo per Total Aset',
        'tagihan_akseptasi_per_total_aset' : 'Tagihan Akseptasi per Total Aset',
        'kyd_dan_pembiayaan_syariah_per_total_aset' : 'KYD dan Pembiayaan Syariah per Total Aset',
        'ckpn_aset_keuangan_per_kyd_dan_pembiayaan_syariah' : 'CKPN Aset Keuangan per KYD dan Pembiayaan Syariah',

        # Fitur dari Liabilitas
        'casa_ratio' : 'CASA Ratio',
        'rim_ratio' : 'RIM Ratio',

        # Fitur dari Modal
        'kpmm_per_car' : 'KPMM per CAR',
        'kpmm_cet1' : 'KPMM CET-1',
        'modal_terhadap_aset' : 'Modal terhadap Aset',
        'modal_terhadap_kredit_bersih' : 'Modal terhadap Kredit Bersih',
        'other_comprehensive_income_to_equity' : 'Other Comprehensive Income',

        # Fitur dari Kualitas Aset
        'ckpn_per_kredit_restruk' : 'Total CKPN per Kredit Restruk',
        'ckpn_stage_2_3_per_kredit_restruk' : 'CKPN Stage 2 & 3 per Kredit Restruk',
        'kredit_bermasalah_dan_restruk_per_kredit_yang_diberikan' : 'Kredit yang Restruk + Kredit Bermasalah non Restruk per Kredit yang Diberikan',
        'kredit_restruk_per_modal_inti' : 'Kredit yang Restruk per Modal Inti',
        'laba_per_kredit_bermasalah_non_restruk' : 'Laba per Kredit Bermasalah non Restruk',
        'laba_per_kredit_restruk' : 'Laba per Kredit Restruk',
        'total_npl_dan_restruk_npl_per_kredit_yang_diberikan' : 'LAR Ratio',

        # Fitur dari Laba Rugi
        # 'other_comprehensive_income' : 'Other Comprehensive Income',
        'kredit_restruk_per_pendapatan_bunga' : 'Kredit Restruk per Pendapatan Bunga',

        # Fitur dari LCR dan NSFR
        'lcr' : 'LCR',
        'nsfr' : 'NSFR',
    }

    return(dict_rasio)

# ----------------------------------------------------------------------------------------

# Code for numeric data

def import_numerik() -> pd.DataFrame:
    """
    Import all Rasio data into one dataframe
    """

    exclude_cols = [
        'posisi',
        'company_name',
        'kbmi_type',
        'year',
        'quarter',
        'year_quarter',
        'company_date',
    ]
    
    # Path to this file's folder ("data")
    base_path = Path(__file__).parent

    # Build absolute paths to the Excel files
    file4 = base_path / "summarized fitur Numeric - KBMI 4.xlsx"
    file2 = base_path / "summarized fitur Numeric - KBMI 2.xlsx"
    file3 = base_path / "summarized fitur Numeric - KBMI 3.xlsx"

    # Read all data files
    df_kbmi_4 = pd.read_excel(file4)
    df_kbmi_2 = pd.read_excel(file2)
    df_kbmi_3 = pd.read_excel(file3)

    # df_aset_4 = pd.read_excel(file_aset_4)

    # Combining df rasio KBMI 1 and KBMI 4
    df_combined_kbmi_2_3_4 = pd.concat([df_kbmi_4, df_kbmi_2, df_kbmi_3], axis=0, join="outer", ignore_index=True)

    # # Combining df with df_aset_4
    # df = merge_two_df(df, df_aset_4, on=['posisi', 'company_name'], exclude_cols=exclude_cols)

    return df_combined_kbmi_2_3_4

def import_fitur_numerik() -> list :
    fitur_numerik = [
        'total_ckpn_stage_2_dan_3',
        'total_npl_dan_restruk_npl',
        'total_kredit_yang_diberikan',
    ]

    return(fitur_numerik)

def import_dictionary_numerik() -> dict :
    dict_numerik = {
        'total_ckpn_stage_2_dan_3': 'CKPN Stage 2 dan 3',
        'total_npl_dan_restruk_npl': 'Total NPL dan Restruk NPL',
        'total_kredit_yang_diberikan' : 'Total Kredit yang Diberikan',
    }

    return(dict_numerik)