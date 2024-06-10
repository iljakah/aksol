import io
import pandas as pd
import streamlit as st
from datenimport import load_csv


def df_metadata(csv_df):
    datacols = csv_df.loc[:, csv_df.notnull().any()].columns.to_list()
    nondatacols = csv_df.loc[:, csv_df.isna().all()].columns.to_list()

    return (datacols, nondatacols)


def data_to_fileobject(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer)
    return buffer


def update_export_df(df, with_nan, bool_val):
    df_export = df.copy(deep=True)
    if not with_nan:
        df_export = df_export.dropna(axis=1, how='all')

    if bool_val == 'Ja':
        for col in df_export.select_dtypes(include=['boolean']):
            df_export[col] = df_export[col].map({True:bool_val}).astype('string')
    elif bool_val == '1':
        for col in df_export.select_dtypes(include=['boolean']):
            df_export[col] = df_export[col].map({True:1}).astype('Int32')

    return df_export

TITEL = "AKS-Online Klartext"

st.set_page_config(
    page_title=TITEL,
    layout="wide",
    page_icon=":pushpin:")

if 'df_main' not in st.session_state:
    st.session_state['df_main'] = pd.DataFrame()
if 'df_exp' not in st.session_state:
    st.session_state['df_exp'] = pd.DataFrame()

st.markdown(f"### {TITEL}")
col1, col2 = st.columns([10,3])
col11, col12 = col1.columns(2)

col2.markdown("__:blue[Exporteinstellungen]__ :gear:")
chknan = col2.checkbox(label="leere Spalten",
                       value=True,
                       key='chk_nan',
                       help="Sollen Spalten ohne Daten auch exportiert werden?")

chkbool = col2.radio(label="exportiere Feldtyp _'Checkbox'_ als:",
                     options=["True [xlsx=wahr()]", "1", "Ja"],
                     key='chk_bool',
                     help="Wie sollen Boolean-Wert exportiert werden")

dateien = col11.file_uploader(label="AKS-Online CSV hochladen", type='csv',
                              accept_multiple_files=True)

if len(dateien) == 2:
    st.session_state['df_main'] = load_csv(dateien[0], dateien[1])
    st.session_state['df_exp'] = update_export_df(st.session_state['df_main'],
                                                  chknan, chkbool)

    view_df = col1.dataframe(st.session_state['df_exp'], key='df_exp')
    df_file_buffer = data_to_fileobject(st.session_state['df_exp'])

    dl_name = f"{dateien[0].name[:-4]}_klartext.xlsx"
    col12.write(dl_name)

    col12.download_button(label='Download XSLX',
                          file_name=dl_name,
                          data=df_file_buffer,
                          mime='xlsx')
