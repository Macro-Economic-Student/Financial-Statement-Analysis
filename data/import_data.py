import pandas as pd
from pathlib import Path

def import_rasio() -> pd.DataFrame:
    """
    Import all Rasio data into one dataframe
    """
    # Path to this file's folder ("data")
    base_path = Path(__file__).parent

    # Build absolute paths to the Excel files
    file1 = base_path / "summarized rasio - KBMI 1.xlsx"
    file4 = base_path / "summarized rasio - KBMI 4.xlsx"

    df_kbmi_1 = pd.read_excel(file1)
    df_kbmi_1 = df_kbmi_1.drop(columns=["sort_key"], errors="ignore")

    df_kbmi_4 = pd.read_excel(file4)

    df = pd.concat([df_kbmi_1, df_kbmi_4], axis=0, join="outer", ignore_index=True)
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
    }

    return(dict_rasio)
