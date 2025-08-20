import pandas as pd

def import_rasio()-> pd.DataFrame :
    """
    Import all Rasio data into one dataframe
    """
    df_kbmi_1 = pd.read_excel("summarized rasio - KBMI 1.xlsx")
    df_kbmi_1 = df_kbmi_1.drop(columns=["sort_key"], errors="ignore")

    df_kbmi_4 = pd.read_excel("summarized rasio - KBMI 4.xlsx")

    df = pd.concat([df_kbmi_1, df_kbmi_4], axis=0, join="outer", ignore_index=True)
    
    return(df)