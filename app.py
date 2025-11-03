import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date

# 1. CARREGAMENTO DOS DADOS
dados = {
    'Ano': [2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023],
    'Região': ['Sul', 'Sul', 'Sul', 'Sul', 'Sudeste', 'Sudeste', 'Sudeste', 'Sudeste'],
    'Internações': [1500, 1650, 1800, 1950, 5000, 5200, 5450, 5600]
}

df = pd.DataFrame(dados)

# Dados para os cartões de indicadores
atendimentos_hoje = 12847
receita_gerada = 2800000
pacientes_unicos = 8934
tempo_medio_atendimento = '2h 15min'

# Dados para o gráfico de evolução de atendimentos
df_evolucao = pd.DataFrame({
    'data': pd.to_datetime(pd.date_range(start='2025-08-26', end='2025-09-22')),
    'Internacoes': np.random.randint(200, 500, size=28),
    'Procedimentos': np.random.randint(150, 400, size=28),
    'Pedriatria': np.random.randint(50, 200, size=28)
})

# Dados para a tabela de hospitais
df_hospitais = pd.DataFrame({
    'Hospital': ['Hospital Municipal São José', 'Hospital Regional Norte', 'Hospital Geral Sul'],
    'Cidade': ['São Paulo', 'Brasília', 'Porto Alegre'],
    'Região': ['Sudeste', 'Centro-Oeste', 'Sul'],
    'Leitos': [245, 180, 310],
    'Ocupação': [0.78, 0.65, 0.92],
    'Atendimentos': [1245, 892, 1550],
    'Receita': ['R$ 295.000', 'R$ 198.000', 'R$ 350.000'],
    'Status': ['Ativo', 'Ativo', 'Ativo']
})


# 2. CONFIGURAÇÃO DO DASH
app = dash.Dash(__name__, assets_folder='assets')

# 3. LAYOUT DA INTERFACE (CONSTRUÇÃO DO HTML COM PYTHON)
app.layout = html.Div(children=[
    
    # Seção de Filtros
    html.Div(className='header-section', children=[
        html.H2('Filtros', className='section-title'),
        html.Div(className='filter-group', children=[
            html.Div(className='filter-item', children=[
                html.Label('Período'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=date(2025, 8, 26),
                    end_date=date(2025, 9, 22),
                    display_format='DD/MM/YYYY'
                )
            ]),
            html.Div(className='filter-item', children=[
                html.Label('Categoria'),
                dcc.Dropdown(
                    id='categoria-dropdown',
                    options=[{'label': 'Todas as categorias', 'value': 'todas'}],
                    value='todas'
                )
            ]),
            html.Div(className='filter-item', children=[
                html.Label('Região'),
                dcc.Dropdown(
                    id='regiao-dropdown',
                    options=[{'label': 'Todas as regiões', 'value': 'todas'}],
                    value='todas'
                )
            ]),
            html.Button('Limpar', id='limpar-filtros-button')
        ])
    ]),
    
    # Seção de Indicadores (Cards)
    html.Div(className='indicators-section', children=[
        html.H2('Visão Geral - Últimos 30 dias', className='section-title'),
        html.Div(className='cards-container', children=[
            # Card de Atendimentos
            html.Div(className='card indicator-card', children=[
                html.H3('Atendimentos', className='card-title'),
                html.P(f'{atendimentos_hoje:,}', className='card-value'),
                html.Span('+8.2% vs período anterior', className='card-change')
            ]),
            # Card de Receita
            html.Div(className='card indicator-card', children=[
                html.H3('Receita Gerada', className='card-title'),
                html.P(f'R$ {receita_gerada / 1000000:.1f} mi', className='card-value'),
                html.Span('+12.5% em procedimentos', className='card-change')
            ]),
            # Card de Pacientes
            html.Div(className='card indicator-card', children=[
                html.H3('Pacientes Únicos', className='card-title'),
                html.P(f'{pacientes_unicos:,}', className='card-value'),
                html.Span('+5.1% cadastrados', className='card-change')
            ]),
            # Card de Tempo Médio
            html.Div(className='card indicator-card', children=[
                html.H3('Tempo Médio', className='card-title'),
                html.P(tempo_medio_atendimento, className='card-value'),
                html.Span('-8.3% de atendimento', className='card-change')
            ])
        ])
    ]),
    
    # Seção de Gráficos de Evolução
    html.Div(className='chart-section', children=[
        html.Div(className='chart-item', children=[
            html.H2('Evolução de Atendimentos', className='section-title'),
            dcc.Graph(
                id='evolucao-atendimentos-grafico',
                figure=px.line(
                    df_evolucao, 
                    x='data', 
                    y=['Internacoes', 'Procedimentos', 'Pedriatria'], 
                    title='Evolução de Atendimentos por dia nos últimos 30 dias',
                    labels={'value': 'Atendimentos', 'variable': 'Tipo de Atendimento'}
                )
            )
        ]),
        html.Div(className='chart-item', children=[
            html.H2('Receita Gerada', className='section-title'),
            # Gráfico de Área para Receita
            dcc.Graph(
                id='receita-gerada-grafico',
                figure=px.area(
                    df_evolucao,
                    x='data',
                    y=['Internacoes', 'Procedimentos', 'Pedriatria'],
                    title='Receita diária dos procedimentos SUS',
                    labels={'value': 'Receita', 'variable': 'Fonte de Receita'}
                )
            )
        ])
    ]),

    # Seção da Tabela
    html.Div(className='table-section', children=[
        html.H2('Hospitais da Rede SUS', className='section-title'),
        html.Div(className='table-container', children=[
            html.Table(children=[
                html.Thead(
                    html.Tr([html.Th(col) for col in df_hospitais.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(
                            html.Div(str(df_hospitais.iloc[i][col]), className='status-' + str(df_hospitais.iloc[i]['Status']).lower())
                            if col == 'Status' else
                            str(df_hospitais.iloc[i][col])
                        ) for col in df_hospitais.columns
                    ]) for i in range(len(df_hospitais))
                ])
            ])
        ])
    ])
])

# 4. RODAR O SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)