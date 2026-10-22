import pandas as pd
df = pd.read_excel('Visão CL - Histórico.xlsx')
for idx, r in df.iterrows():
    loja = r.iloc[0]
    fmt = r.iloc[1]
    e1 = r.iloc[9]
    e2 = r.iloc[10]
    e3 = r.iloc[11]
    e4 = r.iloc[12]
    # Sum of numbers if numeric
    vals = [e1, e2, e3, e4]
    num_vals = [v for v in vals if isinstance(v, (int, float))]
    
    # Check date difference: Inauguração - Contrato
    c_dt = r.iloc[2]
    i_dt = r.iloc[6]
    diff_days = (i_dt - c_dt).days if pd.notnull(c_dt) and pd.notnull(i_dt) else None
    
    # Check date difference: Inauguração - Solicitação
    s_dt = r.iloc[3]
    diff_from_solic = (i_dt - s_dt).days if pd.notnull(s_dt) and pd.notnull(i_dt) else None
    
    print(f"{loja:<32} | E1:{str(e1):>4} E2:{str(e2):>12} E3:{str(e3):>12} E4:{str(e4):>12} | Sum:{sum(num_vals):>4} | Inaug-Contr:{diff_days} | Inaug-Solic:{diff_from_solic}")
