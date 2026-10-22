import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Configurações de tipografia e estilo
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

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

# Paleta exata de regras de negócio
COLOR_PURPLE = '#7C3AED'      # Roxo: Etapa 1 Antecipado (< 0d)
COLOR_GREEN = '#16A34A'       # Verde: Etapa 1 (<= 7d) e Etapa 2 (<= 30d)
COLOR_RED = '#DC2626'         # Vermelho: Atraso (> 7d na E1, > 30d na E2/E3)
COLOR_ORANGE = '#FB923C'      # Laranja Claro: Etapa 3 no prazo (<= 30d)
COLOR_YELLOW = '#EAB308'      # Amarelo/Alerta: Etapa 4 alto risco (< 90d)
COLOR_DARK_GREEN = '#15803D'  # Verde Escuro: Etapa 4 saudável (>= 90d)
COLOR_HATCH = '#94A3B8'       # Cinza / Plano de Ação

shops = []

for idx, r in df.iterrows():
    loja = fix_name(r.iloc[0])
    fmt = r.iloc[1]
    e1 = r.iloc[9]
    e2 = r.iloc[10]
    e3 = r.iloc[11]
    e4 = r.iloc[12]
    
    # Etapa 1
    if isinstance(e1, (int, float)):
        e1_num = int(e1)
        if e1_num < 0:
            e1_col = COLOR_PURPLE
        elif e1_num > 7:
            e1_col = COLOR_RED
        else:
            e1_col = COLOR_GREEN
        e1_txt = f"{e1_num}d"
        e1_w = max(6, abs(e1_num))
    else:
        e1_num = 0
        e1_col = COLOR_HATCH
        e1_txt = str(e1)
        e1_w = 12

    # Etapa 2
    if isinstance(e2, (int, float)):
        e2_num = int(e2)
        if e2_num > 30:
            e2_col = COLOR_RED
        else:
            e2_col = COLOR_GREEN
        e2_txt = f"{e2_num}d"
        e2_w = max(6, e2_num)
        e2_is_plan = False
    else:
        e2_num = 0
        e2_col = COLOR_HATCH
        e2_txt = "Ação"
        e2_w = 18
        e2_is_plan = True

    # Etapa 3
    if isinstance(e3, (int, float)):
        e3_num = int(e3)
        if e3_num > 30:
            e3_col = COLOR_RED
        else:
            e3_col = COLOR_ORANGE
        e3_txt = f"{e3_num}d"
        e3_w = max(6, e3_num)
        e3_is_plan = False
    else:
        e3_num = 0
        e3_col = COLOR_HATCH
        e3_txt = "Ação"
        e3_w = 18
        e3_is_plan = True

    # Etapa 4
    if isinstance(e4, (int, float)):
        e4_num = int(e4)
        if e4_num < 90:
            e4_col = COLOR_YELLOW
        else:
            e4_col = COLOR_DARK_GREEN
        e4_txt = f"{e4_num}d"
        e4_w = max(6, e4_num)
        e4_is_plan = False
    else:
        e4_num = 0
        e4_col = COLOR_HATCH
        e4_txt = "Ação"
        e4_w = 18
        e4_is_plan = True

    # Total acumulado
    nums = [v for v in [e1, e2, e3, e4] if isinstance(v, (int, float))]
    tot = sum(nums)
    if e2_is_plan or e3_is_plan or e4_is_plan:
        tot_str = f"{tot}d + Ação"
    else:
        tot_str = f"{tot}d"

    shops.append({
        'loja': loja,
        'fmt': fmt,
        'label': f"{loja}  [{fmt}]",
        'e1_w': e1_w, 'e1_col': e1_col, 'e1_txt': e1_txt,
        'e2_w': e2_w, 'e2_col': e2_col, 'e2_txt': e2_txt, 'e2_plan': e2_is_plan,
        'e3_w': e3_w, 'e3_col': e3_col, 'e3_txt': e3_txt, 'e3_plan': e3_is_plan,
        'e4_w': e4_w, 'e4_col': e4_col, 'e4_txt': e4_txt, 'e4_plan': e4_is_plan,
        'total_str': tot_str,
        'total_days': tot
    })

# Inverter para que o primeiro item fique no topo
shops = list(reversed(shops))
n = len(shops)

fig = plt.figure(figsize=(20, 14), dpi=220, facecolor='#F8FAFC')
ax = fig.add_axes([0.22, 0.16, 0.74, 0.74]) # [left, bottom, width, height]
ax.set_facecolor('#FFFFFF')

y_pos = np.arange(n)
h = 0.65

for i, s in enumerate(shops):
    y = y_pos[i]
    x = 0
    
    # E1
    w1 = s['e1_w']
    ax.barh(y, w1, left=x, height=h, color=s['e1_col'], edgecolor='#FFFFFF', linewidth=1.5, zorder=3)
    ax.text(x + w1/2, y, s['e1_txt'], ha='center', va='center', color='white', fontweight='bold', fontsize=9, zorder=4)
    x += w1
    
    # E2
    w2 = s['e2_w']
    hatch2 = '///' if s['e2_plan'] else None
    ax.barh(y, w2, left=x, height=h, color=s['e2_col'], hatch=hatch2, edgecolor='#FFFFFF', linewidth=1.5, zorder=3)
    c2_txt = '#0F172A' if s['e2_plan'] else 'white'
    ax.text(x + w2/2, y, s['e2_txt'], ha='center', va='center', color=c2_txt, fontweight='bold', fontsize=8.5, zorder=4)
    x += w2
    
    # E3
    w3 = s['e3_w']
    hatch3 = '///' if s['e3_plan'] else None
    ax.barh(y, w3, left=x, height=h, color=s['e3_col'], hatch=hatch3, edgecolor='#FFFFFF', linewidth=1.5, zorder=3)
    c3_txt = '#0F172A' if s['e3_plan'] else 'white'
    ax.text(x + w3/2, y, s['e3_txt'], ha='center', va='center', color=c3_txt, fontweight='bold', fontsize=8.5, zorder=4)
    x += w3
    
    # E4
    w4 = s['e4_w']
    hatch4 = '///' if s['e4_plan'] else None
    ax.barh(y, w4, left=x, height=h, color=s['e4_col'], hatch=hatch4, edgecolor='#FFFFFF', linewidth=1.5, zorder=3)
    c4_txt = '#0F172A' if s['e4_plan'] or s['e4_col'] == COLOR_YELLOW else 'white'
    ax.text(x + w4/2, y, s['e4_txt'], ha='center', va='center', color=c4_txt, fontweight='bold', fontsize=8.5, zorder=4)
    x += w4
    
    # Total de Dias no final da barra
    badge_bg = '#FEF3C7' if 'Ação' in s['total_str'] else '#F1F5F9'
    badge_border = '#F59E0B' if 'Ação' in s['total_str'] else '#CBD5E1'
    badge_color = '#B45309' if 'Ação' in s['total_str'] else '#0F172A'
    
    ax.text(x + 5, y, s['total_str'], ha='left', va='center',
            color=badge_color, fontweight='bold', fontsize=10, zorder=4,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=badge_bg, edgecolor=badge_border, linewidth=1.0))

# Eixos
ax.set_yticks(y_pos)
ax.set_yticklabels([s['label'] for s in shops], fontsize=10, fontweight='bold', color='#1E293B')
ax.set_xlabel('Evolução de Dias Acumulados de Execução por Etapa', fontsize=12, fontweight='bold', color='#1E293B', labelpad=12)

# Limites e Grid
ax.set_xlim(0, 310)
ax.set_ylim(-0.7, n - 0.3)
ax.grid(axis='x', color='#E2E8F0', linestyle='--', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Remover bordas superior e direita
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
ax.spines['bottom'].set_color('#CBD5E1')

# Título Superior estilizado KFC
fig.text(0.22, 0.955, "KFC 2026 — Roadmap de Expansão", fontsize=18, fontweight='bold', color='#E4002B')
fig.text(0.22, 0.925, "Painel Executivo de Gerenciamento de Projetos | Gráfico de Gantt Horizontal Empilhado de Dias Acumulados",
         fontsize=12, fontweight='bold', color='#334155')

# Legenda Exaustiva no Rodapé
legend_elements = [
    mpatches.Patch(facecolor=COLOR_PURPLE, edgecolor='white', label='Etapa 1: Antecipado (< 0d) [Roxo — Ganho de Tempo]'),
    mpatches.Patch(facecolor=COLOR_GREEN, edgecolor='white', label='Etapa 1 / 2: No Prazo (E1 ≤ 7d / E2 ≤ 30d) [Verde]'),
    mpatches.Patch(facecolor=COLOR_RED, edgecolor='white', label='Atraso Crítico: E1 > 7d | E2 > 30d | E3 > 30d [Vermelho]'),
    mpatches.Patch(facecolor=COLOR_ORANGE, edgecolor='white', label='Etapa 3: No Prazo (E3 ≤ 30d) [Laranja Claro]'),
    mpatches.Patch(facecolor=COLOR_YELLOW, edgecolor='white', label='Etapa 4: Alto Risco (< 90d até Inauguração) [Amarelo/Alerta]'),
    mpatches.Patch(facecolor=COLOR_DARK_GREEN, edgecolor='white', label='Etapa 4: Prazo Seguro e Saudável (≥ 90d) [Verde Escuro]'),
    mpatches.Patch(facecolor=COLOR_HATCH, hatch='///', edgecolor='white', label='Plano de Ação: Etapa em Aberto / Pendente')
]

leg = fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.59, 0.02),
                 ncol=3, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1',
                 fontsize=10, title="Legenda Oficial de Formatação Condicional de Cores",
                 title_fontsize=11, shadow=True, fancybox=True)
leg.get_title().set_fontweight('bold')

out_file = 'kfc_gantt_roadmap_2026.png'
plt.savefig(out_file, dpi=220, bbox_inches='tight')
print(f"Gráfico aprimorado com sucesso em {out_file}!")
