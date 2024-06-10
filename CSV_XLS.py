#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


# bestimmung des aktuellen Pfades mit os.getcwd()


# In[3]:


#setzen des Arbeitsverzeichnisses
os.chdir('F:\\Ablage\MITARBEITER\Julian\Recherche\Marcel\R-Test\CSV')


# In[4]:


#pandas-bibliothek importieren
import pandas as pd


# In[5]:


#Zuweisung einer Bezeichnung für eine Variable umd diese beim Export genau bezeichnen zu können
gesamt_csv = 'AKS-B-GRUND-GESAMT_10.03.2023.csv'
text_anonaym_csv = 'AKS-B-GRUND-TEXT1_10.03.2023.csv'


# In[6]:


#einladen der CSV
gesamt = pd.read_csv(gesamt_csv, delimiter=',', dtype=str, encoding='latin-1')
#die ersten 5 Zeilen der CSV anzeigen lassen
#gesamt.head(5)


# In[7]:


#einladen der CSV
text_anonym = pd.read_csv(text_anonaym_csv, delimiter=',', dtype=str, encoding='latin-1')
#die ersten 5 Zeilen der CSV anzeigen lassen
#text_anonym.head(5)


# In[8]:


#einladen der CSV mit der bezeichnung für die spalten - wird hier nicht benötigt da es später erfolgt
#kopfzeilen = pd.read_csv('Bez_allg.csv',delimiter=';')
#kopfzeilen.head(5)


# In[9]:


#ort = pd.read_csv('Ort.csv',delimiter=';', dtype=str, usecols=[0,1])
#ort.head(5)


# In[10]:


#mit dieser Funktion wird für jede Spalte einzeln der passende Wert aus der jeweiligen CSV mit den Zellenwerten übernommen. Der Hardcode ist aber "viel" weil es für jeden CSV bzw. Spalte einzeln
#gemacht werden müsste
#gesamt['Ort'] = gesamt['Ort'].map(ort.set_index('Wert')['Bedeutung'])
#gesamt['Ort'].map(ort['Bedeutung']).head(5)
#gesamt['CSV_Liste'] = gesamt['CSV_Liste'].map('Liste'.set_index('Wert')['Bedeutung'])


# In[11]:


#Erstellung einer List mit allen CSVs für den Wert der einzelnen Zellen
#diese ist für den nächsten Schritt notwendig
csv_liste = ['Au', 'Bg', 'BL', 'Bz', 'Df', 
             'E', 'Eg', 'Ew', 'EZ', 'Ga', 
             'GArt', 'GB', 'Gg', 'GH', 'Gk', 
             'Gmrk(HL)', 'gN', 'Gs', 'Hz', 'K', 
             'Lage', 'Lg', 'LZ', 'M', 'OF', 
             'ÖM', 'Ort', 'Pakete', 'Pg', 'Pga', 
             'pN', 'RÖ', 'Sa', 'Se', 'SL',
             'St', 'Stela', 'SW', 'TaN', 'TNA',
             'TypEN', 'Um', 'VA', 'Vf', 'Vg',
             'W', 'WA', 'WL', 'WT', 'Zs']


# In[12]:


#Zuordnung der einzelnen Zellenwerte
#dabei wird "csv_name" der erste Wert aus "csv_liste" zugeordnet z.B. 'Au'
#dann wir geschaut ob, 'Au' in den Spalten der Ausgangs-CSV vorhanden ist - wenn ja, dann:
#print gibt den inhalt der variable csv_name aus (weiß gerade nicht mehr wofür das wichtig war, glaube Kontrolle)
#im Anschluss kombinieren wir in csv_dateiname die Bezeichnung der Spalte mit'.csv', das die CSVs mit den Zelleninhalten immer als Spaltenname.csv gespeichert sind
#in die variable csv_daten werden die CSVs mit den Zellenwerten eingeladen
#letzte Zeile: nimm in der ausgangs-pdf die Bezeichnung 'Au' (csv_name) und vergleiche alle Werte in der Spalte mit der CSV 'Au' (csv_daten) und setze den Index auf 'Wert'
#vergleiche den Zellenwerte von der Spalte 'Au' aus der Ausgangs-CSV mit den Zellwenwerten der Spalte 'Wert' der Au_CSV
#wenn wert gleich, ersetze in der Ausgangs-CSV die Werte für 'Au' durch die Werte aus 'Beudeutung' der Au_CSV

#wenn das fertig ist und der Codeblock durchgelaufen ist, beginnt er von vorne für den zweiten Wert der Liste ('Bg') usw.

#wenn der Wert aus der Liste nicht in den Spalten vorhanden ist, wird dieser übersprungen bzw. ohne Ergebnis bearbeitet
for csv_name in csv_liste:
    if csv_name in gesamt.columns:
        print(csv_name)
        csv_dateiname = csv_name+'.csv' 
        csv_daten = pd.read_csv(csv_dateiname, delimiter=';', dtype=str, usecols=[0,1])
        gesamt[csv_name] = gesamt[csv_name].map(csv_daten.set_index('Wert')['Bedeutung'])


# In[13]:


#anzeigen der gesamten geänderten Ausgangs-CSV als Kontrolle
#from IPython.display import display
#pd.options.display.max_columns = None
#display(gesamt)


# In[ ]:





# In[14]:


#einladen und anzeigen der CSV mit den Zuordnungen der Spaltennamen
Bez_allg = pd.read_csv('Bez_allg.csv',delimiter=';', dtype=str, usecols=[0,1,2,3,4])
#display(Bez_allg)


# In[15]:


#löschen er doppelten Werte
#Bez_allg = 
Bez_allg.drop(Bez_allg[(Bez_allg['Kurzname'] == 'Ba') & (Bez_allg['Langname'] == 'Bad')].index, inplace=True)

Bez_allg.drop(Bez_allg[(Bez_allg['Kurzname'] == 'Gz') & (Bez_allg['Langname'] == 'Anzahl Vollgeschosse')].index, inplace=True)

Bez_allg.drop(Bez_allg[(Bez_allg['Kurzname'] == 'wertGF') & (Bez_allg['Teilmarkt UB'] == 'UB')].index, inplace=True)

Bez_allg.drop(Bez_allg[(Bez_allg['Kurzname'] == 'Text (anonymisiert)') & (Bez_allg['Langname'] != 'Text (anonymisiert)')].index, inplace=True)
Bez_allg.drop(Bez_allg[(Bez_allg['Kurzname'] == 'Text (nicht anonymisiert)') & (Bez_allg['Langname'] != 'Zusätzlicher Text (nicht anonymisiert)')].index, inplace=True)


# In[ ]:





# In[ ]:





# In[16]:


#umbenennung der einzelnen Kurzformen der Ausgangs-CSV basierend auf der CSV mit den Zuordnungen (Kurname-Langname)
gesamt.rename(columns=Bez_allg.set_index('Kurzname')['Langname'], inplace=True)
#gesamt


# In[ ]:





# In[17]:


#basierend auf den Nummer (Index) wird die Texspalte aus der CSV mit dem Text an die Ausgangs-CSV angehangen
gesamt = pd.merge(gesamt, text_anonym[['Nr.', 'Text (anonymisiert)']], on='Nr.', how='left')


# In[ ]:





# In[18]:


#die bearbeitete Ausgangs-CSV wird als Excel exportiert und wie die ursprüngliche AUsgangs-CSV bezeichnet
#nimm den Namen der Ausgangs-CSV (siehe Anfang), entferne die letzten vier Stellen (.csv) und hänge .xlsx an, es wird kein globaler Index benötigt 
#gesamt.fillna('kA', inplace=True)
gesamt.to_excel(gesamt_csv[:-4]+'.xlsx', index=False)


# In[ ]:




