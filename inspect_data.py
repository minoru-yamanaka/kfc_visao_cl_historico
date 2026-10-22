import pandas as pd
import sys

df = pd.read_excel('Visão CL - Histórico.xlsx')
print(f"Total rows: {len(df)}")
print("Columns:", [repr(c) for c in df.columns])

for idx, row in df.iterrows():
    loja = row.iloc[0]
    fmt = row.iloc[1]
    dt_contrato = row.iloc[2]
    dt_solic = row.iloc[3]
    dt_emiss = row.iloc[4]
    dt_sap = row.iloc[5]
    dt_inaug = row.iloc[6]
    e1 = row.iloc[9]
    e2 = row.iloc[10]
    e3 = row.iloc[11]
    e4 = row.iloc[12]
    print(f"[{idx+1:02d}] {loja} ({fmt})")
    print(f"     Datas: Contrato={dt_contrato} | Solic={dt_solic} | Emiss={dt_emiss} | SAP={dt_sap} | Inaug={dt_inaug}")
    print(f"     Etapas: E1={e1} | E2={e2} | E3={e3} | E4={e4}")
