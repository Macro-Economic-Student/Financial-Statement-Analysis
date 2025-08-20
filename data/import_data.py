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