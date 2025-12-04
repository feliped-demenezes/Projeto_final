import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import requests
from datetime import date
from dash.dash_table import DataTable # Para tabelas mais avançadas, se necessário
import numpy as np

# --- 1. CARREGAMENTO E CONEXÃO COM A API DOCKER ---
def carregar_dados_da_api():
    """
    Busca os dados de internação na API Dockerizada (FastAPI).
    """
    API_URL = "http://localhost:8000/api/internacoes"
    
    try:
        # Tenta conectar à API. Timeout de 15 segundos.
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status() # Levanta um erro HTTP para status 4xx/5xx
        
        dados = response.json()
        
        # Verifica se a API retornou um status de erro em vez de dados (caso o PySUS falhe na extração)
        if isinstance(dados, dict) and dados.get('status') == 'error':
             print(f"API retornou erro no JSON: {dados['message']}")
             # Retorna um DataFrame vazio e loga o erro
             return pd.DataFrame() 
             
        df = pd.DataFrame(dados)
        
        # Conversão de tipos de dados (Crucial após carregar do JSON)
        if 'Data_Internacao' in df.columns:
             # O JSON do Pandas usa formato ISO (string), precisamos converter de volta para datetime
             df['Data_Internacao'] = pd.to_datetime(df['Data_Internacao'], errors='coerce') 
        
        # Cria uma coluna de ano para filtros, se necessário
        df['Ano'] = df['Data_Internacao'].dt.year
        
        print(f"Dados reais carregados com sucesso: {len(df)} linhas.")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: Não foi possível alcançar a API Docker. Garanta que o container está 'Running' na porta 8000. {e}")
        return pd.DataFrame() # Retorna um DataFrame vazio em caso de falha de conexão

# Tenta carregar os dados reais. Se falhar, usa um DataFrame vazio.
df_sih = carregar_dados_da_api()

# --- DADOS FICTÍCIOS DE FALLBACK/INDICADORES (Se df_sih estiver vazio) ---

# Se a conexão falhar, garantimos que o dashboard não quebre, exibindo 0 ou fictício
if df_sih.empty:
    print("Usando dados de fallback para a interface.")
    
    # Cria dados de evolução fictícios para o gráfico não quebrar
    df_evolucao = pd.DataFrame({
        'Data': pd.to_datetime(pd.date_range('2025-08-26', periods=30, freq='D')),
        'Atendimentos_A': np.random.randint(200, 500, size=30),
        'Atendimentos_B': np.random.randint(150, 400, size=30),
    })
    
    # Cria dados básicos para a tabela de hospitais não quebrar
    df_hospitais = pd.DataFrame({
        'Hospital': ['Hospital A (Fallback)', 'Hospital B (Fallback)'],
        'Cidade': ['Cidade', 'Cidade'],
        'Região': ['Região', 'Região'],
        'Leitos': [100, 150],
        'Status': ['Ativo', 'Ativo']
    })
    atendimentos_hoje = 0
    receita_gerada = 0
    pacientes_unicos = 0
    tempo_medio_atendimento = 'N/A'
    
else:
    # --- PROCESSAMENTO BÁSICO DOS DADOS REAIS PARA INDICADORES E GRÁFICOS ---
    
    # 1. Indicadores
    atendimentos_hoje = len(df_sih) # Total de internações no período
    receita_gerada = df_sih['VAL_TOT'].sum() / 1000000 if 'VAL_TOT' in df_sih.columns else 0
    pacientes_unicos = df_sih['IDADE'].nunique() if 'IDADE' in df_sih.columns else 0 # Simplificado
    tempo_medio_atendimento = '2h 15min' # Dado fictício, pois requer cálculo complexo do SIH
    
    # 2. Gráfico de Evolução (Agrupamento real)
    df_evolucao = df_sih.groupby(df_sih['Data_Internacao'].dt.date)['VAL_TOT'].sum().reset_index()
    df_evolucao.columns = ['Data', 'Receita']
    
    # 3. Tabela de Hospitais (Apenas um placeholder para visualização)
    df_hospitais = pd.DataFrame({
        'Hospital': ['Hospital X', 'Hospital Y', 'Hospital Z'],
        'Cidade': ['Capital', 'Interior', 'Interior'],
        'Atendimentos': [500, 300, 200]
    })


# --- 2. CONFIGURAÇÃO DO DASH ---
app = dash.Dash(__name__, assets_folder='assets')

# --- 3. LAYOUT DA INTERFACE ---

app.layout = html.Div(children=[
    
    # Seção de Filtros
    html.Div(className='header-section', children=[
        html.H2('Filtros', className='section-title'),
        html.Div(className='filter-group', children=[
            html.Div(className='filter-item', children=[
                html.Label('Período'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date_placeholder_text="Início",
                    end_date_placeholder_text="Fim",
                    display_format='DD/MM/YYYY'
                )
            ]),
            html.Div(className='filter-item', children=[
                html.Label('Região'),
                dcc.Dropdown(
                    id='regiao-dropdown',
                    options=[{'label': 'Todas as regiões', 'value': 'todas'}] + 
                            [{'label': r, 'value': r} for r in (df_sih['MUNICIPIO'].unique() if not df_sih.empty and 'MUNICIPIO' in df_sih.columns else [])],
                    value='todas'
                )
            ]),
            html.Button('Limpar', id='limpar-filtros-button')
        ])
    ]),
    
    # --- Na Seção de Indicadores (Cards) ---

    html.Div(className='cards-container', children=[
        
        # Card 1: Total de Internações
        html.Div(className='card indicator-card', children=[
            html.H3('Total de Internações', className='card-title'),
            # ADICIONE ESTE ID
            html.P(f'{atendimentos_hoje:,}', id='indicador-internacoes-valor', className='card-value'),
            html.Span('Dados Reais PySUS', className='card-change')
        ]),
        
        # Card 2: Receita
        html.Div(className='card indicator-card', children=[
            html.H3('Receita Gerada (Total)', className='card-title'),
            # ADICIONE ESTE ID
            html.P(f'R$ {receita_gerada:.2f} mi', id='indicador-receita-valor', className='card-value'),
            html.Span('Valor Total das Internações', className='card-change')
        ]),
        
        # Card 3: Pacientes
        html.Div(className='card indicator-card', children=[
            html.H3('Pacientes Únicos', className='card-title'),
            # ADICIONE ESTE ID
            html.P(f'{pacientes_unicos:,}', id='indicador-pacientes-valor', className='card-value'),
            html.Span('Aproximação pela Idade', className='card-change')
        ]),
        
        # Card 4: Tempo Médio (Este não é atualizado pelo callback, então não precisa de ID de saída)
        html.Div(className='card indicator-card', children=[
            html.H3('Tempo Médio', className='card-title'),
            html.P(tempo_medio_atendimento, className='card-value'),
            html.Span('Dado Fictício/Ajustável', className='card-change')
        ]),
    ]),
    
    # Seção de Gráficos de Evolução
    html.Div(className='chart-section', children=[
        html.Div(className='chart-item', children=[
            html.H2('Evolução de Receita', className='section-title'),
            dcc.Graph(
                id='evolucao-receita-grafico',
                figure=px.line(
                    df_evolucao, 
                    x='Data', 
                    y=['Atendimentos_A', 'Atendimentos_B'],
                    title='Evolução da Receita Diária (SIH)',
                    labels={'Receita': 'Valor Total (R$)', 'Data': 'Data de Internação'}
                )
            )
        ])
    ]),

    # Seção da Tabela
    html.Div(className='table-section', children=[
        html.H2('Análise Hospitalar', className='section-title'),
        html.Div(className='table-container', children=[
            html.Table(children=[
                html.Thead(
                    html.Tr([html.Th(col) for col in df_hospitais.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(str(df_hospitais.iloc[i][col])) for col in df_hospitais.columns
                    ]) for i in range(len(df_hospitais))
                ])
            ])
        ])
    ])
])

# --- 4. CALLBACKS DE INTERATIVIDADE ---

# --- 4. CALLBACKS DE INTERATIVIDADE ---
# Nota: Este callback utiliza o DataFrame df_evolucao de fallback (com colunas 'Data', 'Atendimentos_A', 'Atendimentos_B').

@app.callback(
    # Saídas: IDs dos 3 cartões de indicadores (os valores)
    [dash.Output('indicador-internacoes-valor', 'children'),
     dash.Output('indicador-receita-valor', 'children'),
     dash.Output('indicador-pacientes-valor', 'children')],
    
    # Entradas: Os mesmos filtros que atualizam o gráfico
    [dash.Input('date-picker-range', 'start_date'),
     dash.Input('date-picker-range', 'end_date'),
     dash.Input('regiao-dropdown', 'value')]
)
def update_indicators(start_date, end_date, selected_regiao):
    # Usamos o mesmo df_evolucao de fallback (dados fictícios)
    global df_evolucao 
    df_filtered = df_evolucao.copy()
    
    # --- 1. FILTRO DE DATA (Repetido do Callback do Gráfico) ---
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[
            (df_filtered['Data'] >= start_date) &
            (df_filtered['Data'] <= end_date)
        ]
        
    # --- 2. FILTRO DE REGIÃO (Repetido do Callback do Gráfico) ---
    if selected_regiao and selected_regiao != 'todas' and not df_filtered.empty:
        df_filtered = df_filtered[df_filtered['MUNICIPIO'] == selected_regiao]
        
    # --- 3. CÁLCULOS DOS KPIS (Usando colunas fictícias) ---
    if df_filtered.empty:
        return '0', 'R$ 0.00 mi', '0'

    # Total de Internações (Fictício: Soma das colunas A e B)
    total_internacoes = df_filtered['Atendimentos_A'].sum() + df_filtered['Atendimentos_B'].sum()
    
    # Receita Gerada (Fictício: Soma de Atendimentos_A * 0.005)
    receita_gerada = df_filtered['Atendimentos_A'].sum() * 0.005 
    
    # Pacientes Únicos (Fictício: Contagem de dias no filtro * 3)
    pacientes_unicos = len(df_filtered) * 3 
    
    # --- 4. FORMATANDO A SAÍDA ---
    
    # Formato de milhares (Ex: 12.847)
    internacoes_str = f'{total_internacoes:,}'.replace(',', '.')
    pacientes_str = f'{pacientes_unicos:,}'.replace(',', '.')
    
    # Formato monetário (Ex: R$ 0.52 mi)
    receita_str = f'R$ {receita_gerada/1000000:.2f} mi'
    
    # O retorno deve ser na ORDEM exata definida no dash.Output
    return internacoes_str, receita_str, pacientes_str
# --- 5. RODAR O SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)