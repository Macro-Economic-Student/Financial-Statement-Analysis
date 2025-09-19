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

    # Build absolute paths to the Excel files
    file1 = base_path / "summarized rasio - KBMI 1.xlsx"
    file4 = base_path / "summarized rasio - KBMI 4.xlsx"
    file_aset_4 = base_path / "summarized fitur aset - KBMI 4.xlsx"
    file_liabilitas_4 = base_path / "summarized fitur liabilitas - KBMI 4.xlsx"
    file_kpmm_4 = base_path / "summarized fitur kpmm - KBMI 4.xlsx"
    file_kualitas_4 = base_path / "summarized fitur Kualitas Aset - KBMI 4.xlsx"

    # Read all data files
    df_kbmi_1 = pd.read_excel(file1)
    df_kbmi_1 = df_kbmi_1.drop(columns=["sort_key"], errors="ignore")

    df_kbmi_4 = pd.read_excel(file4)

    df_aset_4 = pd.read_excel(file_aset_4)

    df_liabilitas_4 = pd.read_excel(file_liabilitas_4)

    df_kpmm_4 = pd.read_excel(file_kpmm_4)

    df_kualitas_4 = pd.read_excel(file_kualitas_4)

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

    return df

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

        # Fitur dari Kualitas Aset
        'ckpn_per_kredit_restruk',
        'ckpn_stage_2_3_per_kredit_restruk',
        'kredit_bermasalah_dan_restruk_per_kredit_yang_diberikan',
        'kredit_restruk_per_modal_inti',
        'laba_per_kredit_bermasalah_non_restruk',
        'laba_per_kredit_restruk',
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

        # Fitur dari Kualitas Aset
        'ckpn_per_kredit_restruk' : 'Total CKPN per Kredit Restruk',
        'ckpn_stage_2_3_per_kredit_restruk' : 'CKPN Stage 2 & 3 per Kredit Restruk',
        'kredit_bermasalah_dan_restruk_per_kredit_yang_diberikan' : 'Kredit yang Restruk + Kredit Bermasalah non Restruk per Kredit yang Diberikan',
        'kredit_restruk_per_modal_inti' : 'Kredit yang Restruk per Modal Inti',
        'laba_per_kredit_bermasalah_non_restruk' : 'Laba per Kredit Bermasalah non Restruk',
        'laba_per_kredit_restruk' : 'Laba per Kredit Restruk',
    }

    return(dict_rasio)
