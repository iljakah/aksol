from itertools import chain
import pandas as pd


def flatten(listoflists):
    return list(chain.from_iterable(listoflists))


def commoncols(columnames, dataframe):
    return list(set(columnames).intersection(dataframe.columns.to_list()))


def txt2dict(fname, sep=';'):
    with open(fname, 'r', encoding='utf-8-sig') as fh:
        _ = fh.readline() # Kopfzeile überspringen
        d = dict(line.rstrip().split(sep) for line in fh)
    return d


def substitute(df, colname):
    if colname in df.columns:
        csvname = f"./CSV/{colname}.csv"
        substdict = txt2dict(fname=csvname)
        df[colname] = df[colname].map(substdict)


def load_csv(csv_gesamt, csv_mit_text):
    data = pd.read_csv(csv_gesamt, delimiter=',', dtype=str, encoding='latin-1')
    data_w_txt = pd.read_csv(csv_mit_text,delimiter=',', dtype=str, encoding='latin-1')
    data_full = pd.merge(data, data_w_txt,how='inner')

    headers = pd.read_csv("merkmale.csv", delimiter=';',dtype=str, encoding='utf-8')

    # Festlegen der Spalten die numerische Datentypen enthalten
    numtypes = ['num', 'curr', 'year']
    numcols = [list(headers['kurz'][headers['datentyp'] == numt]) for numt in numtypes]
    numcols = flatten(numcols)
    # nur Spaltennamen behalten, die in Datensatz vorhanden sind
    numcols = commoncols(numcols, data_full)

    # europ. Dezimalzeichen in Daten ersetzen
    data_full[numcols] = data_full[numcols].replace('\\.', '',regex=True)
    data_full[numcols] = data_full[numcols].replace(',', '.',regex=True)

    # Spalten mit numerische in num. Datentypen umwandeln
    for col in numcols:
        data_full[col] = pd.to_numeric(data_full[col], errors='coerce')

    keycols = list(headers['kurz'][headers['datentyp'] == 'key'])

    for keyname in keycols:
        substitute(data_full, keyname)

    boolnames = list(headers['kurz'][headers['datentyp'] == 'bool'])
    boolnames = commoncols(boolnames, data_full)
    for col in data_full[boolnames]:
        data_full[col] = data_full[col].map({'1':True}).astype('boolean')

    # Umbenennen der Spaltennamen in ihre Langform
    data_full = data_full.rename(columns=dict(zip(headers['kurz'],headers['lang'])))
    ## Alle Spalten entfernen die nur leere Einträge haben
    #data_full = data_full.dropna(axis=1, how='all')
    return data_full
