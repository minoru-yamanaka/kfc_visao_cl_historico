# 🍗 KFC 2026 — Roadmap de Expansão

Dashboard executivo de gerenciamento de projetos com **gráfico de Gantt horizontal empilhado** para monitoramento da evolução dos dias acumulados por shopping e praça de expansão no pipeline KFC Brasil 2026.

---

## 📌 Regras Oficiais de Formatação Condicional de Cores

O monitoramento divide cada projeto em 4 etapas cronológicas consecutivas com as seguintes regras de formatação condicional:

| Etapa | Critério | Cor | Significado Operacional |
| :--- | :--- | :--- | :--- |
| **Etapa 1** (Contrato até Solicitação do CNPJ) | `< 0 dias` | 🟣 **Roxo** | **Antecipado:** Solicitação antes do contrato (ganho de tempo) |
| | `≤ 7 dias` | 🟢 **Verde** | **No Prazo:** Solicitação dentro do prazo de 7 dias |
| | `> 7 dias` | 🔴 **Vermelho** | **Atraso:** Solicitação realizada após mais de 7 dias |
| **Etapa 2** (Solicitação até Emissão do CNPJ) | `≤ 30 dias` | 🟢 **Verde** | **No Prazo:** Emissão realizada em até 30 dias |
| | `> 30 dias` | 🔴 **Vermelho** | **Atraso:** Mais de 30 dias decorridos para emissão |
| **Etapa 3** (Emissão do CNPJ até Criação no SAP) | `≤ 30 dias` | 🟠 **Laranja Claro** | **No Prazo:** Cadastro no SAP realizado em até 30 dias |
| | `> 30 dias` | 🔴 **Vermelho** | **Atraso:** Mais de 30 dias decorridos para criação no SAP |
| **Etapa 4** (Criação no SAP até a Inauguração) | `< 90 dias` | 🟡 **Amarelo / Alerta** | **Alto Risco:** Prazo restante inferior a 90 dias até a abertura |
| | `≥ 90 dias` | 🌲 **Verde Escuro** | **Saudável:** Prazo seguro e confortável (≥ 90 dias) para obras |
| **Etapa Pendente** | `Não Possui / Em Aberto` | ⚪ **Listrado / Cinza** | **Plano de Ação:** Acompanhamento prioritário |

---

## 🚀 Como Rodar e Visualizar

### 1. Dashboard Web Interativo (`index.html`)
Abra o arquivo diretamente no navegador com um duplo clique ou execute no terminal:
```powershell
Start-Process index.html
```
* **Recursos:** Filtro dinâmico por formato (FC, FS, IL), filtro por nível de risco, alternância entre visualização empilhada e marco zero alinhado no contrato, modo escuro/claro e modal de auditoria por shopping.

### 2. Gráfico Estático em Imagem de Alta Definição (`kfc_gantt_roadmap_2026.png`)
```powershell
Start-Process kfc_gantt_roadmap_2026.png
```

### 3. Planilha Formatada (`KFC_2026_Roadmap_Dashboard.xlsx`)
```powershell
Start-Process KFC_2026_Roadmap_Dashboard.xlsx
```

---

## 🛠️ Scripts de Atualização de Dados

Caso a planilha original `Visão CL - Histórico.xlsx` seja atualizada:

```powershell
# 1. Processa os dados e aplica as regras
python process_data.py

# 2. Atualiza o dashboard web interativo
python generate_dashboard.py

# 3. Atualiza a imagem do gráfico de Gantt
python generate_gantt_chart.py

# 4. Atualiza a planilha formatada no Excel
python generate_excel_dashboard.py
```

---

## 📁 Estrutura do Repositório

```
├── KFC_logo.svg                      # Logotipo oficial em vetor
├── Visão CL - Histórico.xlsx         # Planilha original com histórico
├── data.json                         # Dados processados e classificados
├── index.html                        # Dashboard web interativo
├── kfc_gantt_roadmap_2026.png        # Gráfico de Gantt renderizado em alta resolução
├── KFC_2026_Roadmap_Dashboard.xlsx   # Planilha Excel com formatação condicional e legenda
├── generate_dashboard.py             # Script construtor do dashboard web
├── generate_gantt_chart.py           # Script construtor da imagem PNG
├── generate_excel_dashboard.py       # Script construtor da planilha formatada
├── process_data.py                   # Script de ingestão e regras de negócio
└── README.md                         # Documentação do projeto
```
