import pandas as pd
import json

df = pd.read_excel('Visão CL - Histórico.xlsx')

def fix_name(s):
    if not isinstance(s, str):
        return s
    replacements = {
        'PRAA DA REPBLICA (SP)': 'PRAÇA DA REPÚBLICA (SP)',
        'FC SHOPPING SO JOS': 'FC SHOPPING SÃO JOSÉ',
        'SH BURITI GUAR': 'SH BURITI GUARÁ',
        'PERUBE': 'PERUÍBE',
        'No Possui': 'Não Possui',
        'Plano de Ao': 'Plano de Ação'
    }
    for k, v in replacements.items():
        if k in s:
            s = s.replace(k, v)
    return s

def classify_stage_1(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return {'color': '#8B5CF6', 'class': 'purple', 'name': 'Roxo', 'status': 'Antecipado (-' + str(abs(int(val))) + 'd)', 'rule': 'Solicitação antes do contrato (ganho de tempo)'}
        elif val > 7:
            return {'color': '#EF4444', 'class': 'red', 'name': 'Vermelho', 'status': 'Atraso (> 7d)', 'rule': 'Atraso (> 7 dias)'}
        else:
            return {'color': '#22C55E', 'class': 'green', 'name': 'Verde', 'status': 'No Prazo (<= 7d)', 'rule': 'No prazo (<= 7 dias)'}
    return {'color': '#94A3B8', 'class': 'gray', 'name': 'Cinza', 'status': str(val), 'rule': 'Sem dados'}

def classify_stage_2(val):
    if isinstance(val, (int, float)):
        if val > 30:
            return {'color': '#EF4444', 'class': 'red', 'name': 'Vermelho', 'status': 'Atraso (> 30d)', 'rule': 'Atraso (> 30 dias)'}
        else:
            return {'color': '#22C55E', 'class': 'green', 'name': 'Verde', 'status': 'No Prazo (<= 30d)', 'rule': 'No prazo (<= 30 dias)'}
    return {'color': '#94A3B8', 'class': 'gray', 'name': 'Cinza', 'status': str(val), 'rule': 'Plano de Ação / Pendente'}

def classify_stage_3(val):
    if isinstance(val, (int, float)):
        if val > 30:
            return {'color': '#EF4444', 'class': 'red', 'name': 'Vermelho', 'status': 'Atraso (> 30d)', 'rule': 'Atraso (> 30 dias)'}
        else:
            return {'color': '#FB923C', 'class': 'light-orange', 'name': 'Laranja Claro', 'status': 'No Prazo (<= 30d)', 'rule': 'No prazo (<= 30 dias)'}
    return {'color': '#94A3B8', 'class': 'gray', 'name': 'Cinza', 'status': str(val), 'rule': 'Plano de Ação / Pendente'}

def classify_stage_4(val):
    if isinstance(val, (int, float)):
        if val < 90:
            return {'color': '#F59E0B', 'class': 'yellow-alert', 'name': 'Amarelo/Alerta', 'status': 'Alto Risco (< 90d)', 'rule': 'Alto risco para a inauguração (< 90 dias)'}
        else:
            return {'color': '#15803D', 'class': 'dark-green', 'name': 'Verde Escuro', 'status': 'Saudável (>= 90d)', 'rule': 'Prazo seguro e saudável (>= 90 dias)'}
    return {'color': '#94A3B8', 'class': 'gray', 'name': 'Cinza', 'status': str(val), 'rule': 'Plano de Ação / Pendente'}

records = []
for idx, r in df.iterrows():
    loja = fix_name(r.iloc[0])
    formato = r.iloc[1]
    dt_contrato = str(r.iloc[2])[:10] if pd.notnull(r.iloc[2]) else ''
    dt_solic = str(r.iloc[3])[:10] if pd.notnull(r.iloc[3]) else ''
    dt_emiss = fix_name(str(r.iloc[4])[:10] if isinstance(r.iloc[4], pd.Timestamp) else str(r.iloc[4]))
    dt_sap = fix_name(str(r.iloc[5])[:10] if isinstance(r.iloc[5], pd.Timestamp) else str(r.iloc[5]))
    dt_inaug = str(r.iloc[6])[:10] if pd.notnull(r.iloc[6]) else ''
    
    e1 = r.iloc[9]
    e2 = r.iloc[10]
    e3 = r.iloc[11]
    e4 = r.iloc[12]
    
    e1_val = int(e1) if isinstance(e1, (int, float)) and not pd.isna(e1) else fix_name(str(e1))
    e2_val = int(e2) if isinstance(e2, (int, float)) and not pd.isna(e2) else fix_name(str(e2))
    e3_val = int(e3) if isinstance(e3, (int, float)) and not pd.isna(e3) else fix_name(str(e3))
    e4_val = int(e4) if isinstance(e4, (int, float)) and not pd.isna(e4) else fix_name(str(e4))
    
    nums = [v for v in [e1_val, e2_val, e3_val, e4_val] if isinstance(v, (int, float))]
    total_acc = sum(nums)
    all_numeric = len(nums) == 4
    
    c1 = classify_stage_1(e1_val)
    c2 = classify_stage_2(e2_val)
    c3 = classify_stage_3(e3_val)
    c4 = classify_stage_4(e4_val)
    
    records.append({
        'id': idx + 1,
        'loja': loja,
        'formato': formato,
        'datas': {
            'contrato': dt_contrato,
            'solicitacao': dt_solic,
            'emissao': dt_emiss,
            'sap': dt_sap,
            'inauguracao': dt_inaug
        },
        'etapa1': {'dias': e1_val, **c1},
        'etapa2': {'dias': e2_val, **c2},
        'etapa3': {'dias': e3_val, **c3},
        'etapa4': {'dias': e4_val, **c4},
        'total_acumulado': total_acc,
        'todas_etapas_concluidas': all_numeric
    })

print(f"Loaded {len(records)} records successfully.")
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)
print("Saved data.json successfully.")
