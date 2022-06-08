
import base64
import plotly.graph_objs as go
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import plotly.express as px



def main_layout() -> html.Div:
    print("Layout")
    return html.Div(style={'border-style': 'none', 'width': '1366px', 'margin': 'auto'},
                    children=[
        html.H2('MutAnTs (Mutation Analysis Tools) Viewer', style={'text-align': 'center'}),
        html.Div(style={'border-style': 'none', 'height': '99%', 'width': '69%', 'float': 'left', 'margin': 'auto'},
                 children=[
            html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'padding': '10px 5px 5px 2px', 'margin': 'auto'},
                     children=[
                    html.P("Filtros:", style={'font-weight': 'bold'}),
                    html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'left', 'margin': 'auto'},
                             children=[
                        html.P("Qualis:", style={'text-align': 'left'}),
                        dcc.Dropdown(
                            app.qualis, app.qualis, multi=True, id='qualis_filter')
                    ]),
                    html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'right', 'margin': 'auto'},
                             children=[
                        html.P("Periódico:", style={'text-align': 'left'}),
                        dcc.Dropdown(
                            app.periodico, app.periodico, multi=True, id='journal_filter')
                    ]),
                    ]),
            html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'padding': '10px 5px 5px 2px', 'margin': 'auto'},
                     children=[
                html.P("Seletores:", style={'font-weight': 'bold'}),
                html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'left', 'margin': 'auto'},
                         children=[
                    html.P("Ano: ", style={'text-align': 'left'}),
                    dcc.RangeSlider(app.ano_min, app.ano_max,
                                    marks={i: f'{i}' for i in range(app.ano_min, app.ano_max, 1 if (
                                        app.ano_max-app.ano_min) < app.LIMIT_SCALE else (app.ano_max-app.ano_min)//app.LIMIT_SCALE)},
                                    value=[app.ano_min, app.ano_max])
                ]),
                html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'right', 'margin': 'auto'},
                         children=[
                    html.P("Citações:", style={'text-align': 'left'}),
                    dcc.RangeSlider(0, app.cit_max,
                                    marks={i: f'{i}' for i in range(
                                        0, app.cit_max, 1 if app.cit_max < app.LIMIT_SCALE else app.cit_max//app.LIMIT_SCALE)},
                                    value=[0, app.cit_max]
                                    )
                ]),
            ]),
            html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'padding': '10px 5px 5px 2px', 'margin': 'auto'},
                     children=[
                html.P("Gráfico:", style={'font-weight': 'bold', 'width':'242'}),
                dcc.Graph(figure=app.fig)
            ]),
        ]),
        html.Div(style={'border-style': 'solid', 'height': '99%', 'width': '28%', 'float': 'left', 'margin': 'auto','padding': '10px 10px 10px 10px'},
                 children=[
                     'conteúdo'
                 ]),
        html.Div(style={'border-style': 'solid', 'height': 'auto', 'width': '99%', 'float': 'left', 'margin': 'auto'},
                 children=[
        html.H3("Disciplina INF 723."),
        html.P("Este trabalho prático foi desenvolvido como parte fundamental\
                    para a avaliação da disciplina Visualização de Dados \
                    do curso de pós graduação Stricto Sensu em Ciência da \
                    Computação pela Universidade Federal de Viçosa - MG."),
        html.H3('Professora:'),
        html.P('Sabrina Silveira'),
        html.H3('Estudantes:'),
        html.P('Cleiton Monteiro - ES89321'),
        html.P('Jeronimo Costa Penha - ES91669'),
                 ]),
        
    ])


def update_graph(df):
    app.fig = px.sunburst(
        df, path=['qualis', 'publication', 'year', 'name'], maxdepth=4, width=900, height=900)


def read_csv(filename):
    print("csv reader")
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the database file.'
        ])
    csv_content_virg = df
    update_graph(df)
    


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.LIMIT_SCALE = 10
app.csv_content_virg = None
app.qualis = ['New York City', 'Montréal', 'San Francisco']
app.periodico = ['New York City', 'Montréal', 'San Francisco']
app.fig = None
app.cit_max = 101
app.ano_min = 2000
app.ano_max = 2022

if __name__ == '__main__':
    read_csv('db/db.csv')
    app.layout = main_layout()
    app.run_server(debug=True)
