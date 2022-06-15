import base64
import json
from numpy import NaN, empty
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
        html.H2('MutAnTs (Mutation Analysis Tools) Viewer',
                style={'text-align': 'center'}),
        html.Div(style={'border-style': 'none', 'height': '99%', 'width': '69%', 'float': 'left', 'margin': 'auto'},
                 children=[
            html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'padding': '10px 5px 5px 2px', 'margin': 'auto'},
                     children=[
                html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'left', 'margin': 'auto'},
                         children=[
                    html.H6("Ano de Publicação:", style={
                            'font-weight': 'bold'}),
                    dcc.RangeSlider(app.ano_min, app.ano_max,
                                    marks={i: f'{i}' for i in range(app.ano_min, app.ano_max, 1 if (
                                        app.ano_max-app.ano_min) < app.LIMIT_SCALE else (app.ano_max-app.ano_min)//app.LIMIT_SCALE)},
                                    value=[app.ano_min, app.ano_max], id='year_slider'),
                    html.P(id='year_range'),
                ]),
                html.Div(style={'border-style': 'none', 'height': '5%', 'width': '49%', 'float': 'right', 'margin': 'auto'},
                         children=[
                    html.H6("Quantidade de Citações:", style={
                            'font-weight': 'bold'}),
                    dcc.RangeSlider(0, app.cit_max,
                                    marks={i: f'{i}' for i in range(
                                        0, app.cit_max, 1 if app.cit_max < app.LIMIT_SCALE else app.cit_max//app.LIMIT_SCALE)},
                                    value=[0, app.cit_max], id='citation_slider'),
                    html.P(id='citation_range'),
                ]),
            ]),
            html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'padding': '10px 5px 5px 2px', 'margin': 'auto'},
                     children=[
                html.H6("Gráfico:", style={
                    'font-weight': 'bold', 'width': '242'}),
                dcc.Graph(figure=app.fig, id='graph-interact',)
            ]),
        ]),
        html.Div(style={'border-style': 'none', 'height': '99%', 'width': '28%', 'float': 'left', 'margin': 'auto', 'padding': '10px 10px 10px 10px'},
                 children=[
            html.H6("Dados da ferramenta: ", style={'font-weight': 'bold'}),
            html.Div([
                html.Div([
                    html.Strong('Nome: '), html.Br(),
                    html.Strong('Periódico: '), html.Br(),
                    html.Strong('Doi: '), html.Br(),
                    html.Strong('Ano: '), html.Br(),
                    html.Strong('Citações: '), html.Br(),
                    html.Strong('Qualis: '), html.Br(),
                    html.Strong('Fator JCR: '), html.Br(),
                ])
            ], id='tools-data')
        ]),
        html.Div(style={'border-style': 'none', 'height': '99%', 'width': '28%', 'float': 'left', 'margin': 'auto', 'padding': '10px 10px 10px 10px'},
                 children=[
            html.H6("Qualis: ", style={'font-weight': 'bold'}),
            html.Div(style={'border-style': 'none', 'width': '100%', 'float': 'left', 'margin': 'auto'},
                     children=[
                dcc.Dropdown(
                    app.qualis, app.qualis, multi=True, id='qualis_filter')
            ]),
        ]),
        html.Div(style={'border-style': 'none', 'height': '99%', 'width': '28%', 'float': 'left', 'margin': 'auto', 'padding': '10px 10px 10px 10px'},
                 children=[
            html.H6("Periódico: ", style={'font-weight': 'bold'}),
            html.Div([
                html.Div(style={'border-style': 'none', 'width': '100%', 'float': 'left', 'margin': 'auto'},
                         children=[
                    dcc.Dropdown(
                        app.periodico, app.periodico, multi=True, id='journal_filter')
                ]),
            ])
        ]),
        html.Div(style={'border-style': 'none', 'height': 'auto', 'width': '99%', 'float': 'left', 'margin': 'auto'},
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
        df, path=['qualis', 'publicacao', 'ano', 'nome'], maxdepth=4, width=900, height=900)
    app.fig.update_layout(clickmode='event+select')


def update_qualis_filter(df):
    print('update qualis filter')
    qualis = []
    for i in df['qualis']:
        if i not in qualis:
            qualis.append(i)
    app.qualis = qualis


def update_periodico_filter(df):
    print('update periodico filter')
    periodico = []
    for i in df['publicacao']:
        if i not in periodico:
            periodico.append(i)
    app.periodico = periodico


def read_csv(filename):
    print("csv reader")
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the database file.'
        ])
    app.df = df
    update_graph(df)
    update_qualis_filter(df)
    update_periodico_filter(df)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.LIMIT_SCALE = 10
app.qualis = []
app.periodico = []
app.fig = None
app.cit_max = 101
app.ano_min = 2000
app.ano_max = 2022


@app.callback(
    Output('tools-data', 'children'),
    Input('graph-interact', 'clickData'))
def filter_graphic(clickData):
    ret = html.Div([
        html.Strong('Nome: '), html.Br(),
        html.Strong('Periódico: '), html.Br(),
        html.Strong('Doi: '), html.Br(),
        html.Strong('Ano: '), html.Br(),
        html.Strong('Citações: '), html.Br(),
        html.Strong('Qualis: '), html.Br(),
        html.Strong('Fator JCR: '), html.Br(),
    ])
    if clickData is None:
        return ret
    tool = clickData['points'][0]['label']
    a = app.df.loc[app.df['nome'] == tool]

    if len(a) > 0:
        ret = html.Div([
            html.Strong("Nome: "),  str(a['nome'].item()), html.Br(),
            html.Strong('Periódico: '), str(a['publicacao'].item()), html.Br(),
            html.Strong('Doi: '), html.A(str(a['link'].item()), href=str(
                a['link'].item()), target="_blank"), html.Br(),
            html.Strong('Ano: '), str(a['ano'].item()), html.Br(),
            html.Strong('Citações: '), str(a['citacoes'].item()), html.Br(),
            html.Strong('Qualis: '), str(a['qualis'].item()), html.Br(),
            html.Strong('Fator JCR: '), str(a['impacto'].item()), html.Br(),
        ])
    return ret


@app.callback(
    Output('graph-interact', 'figure'),
    Input('qualis_filter', 'value'),
    Input('journal_filter', 'value'),
    Input('year_slider', 'value'),
    Input('citation_slider', 'value'))
def filter_graphic(qualis_value, journal_value, year_slider_value, citation_slider_value):
    print('filter_graphic')
    df = app.df
    df = df.loc[(df['ano'] >= (year_slider_value[0])) &
                (df['ano'] <= (year_slider_value[1]))]
    df = df.loc[(df['citacoes'] >= (citation_slider_value[0])) &
                (df['citacoes'] <= (citation_slider_value[1]))]
    df = df.loc[df['qualis'].isin(qualis_value)]
    df = df.loc[df['publicacao'].isin(journal_value)]
    if df is not None:
        fig = px.sunburst(
            df, path=['qualis', 'publicacao', 'ano', 'nome'], maxdepth=4, width=900, height=900)
        app.fig = fig
    return app.fig


@app.callback(
    Output('year_range', 'children'),
    Input('year_slider', 'value'))
def year_range_updater(year_slider_value):
    print('year_range_updater')
    return "Entre os anos de %d e %d" % (int(year_slider_value[0]), int(year_slider_value[1]))


@app.callback(
    Output('citation_range', 'children'),
    Input('citation_slider', 'value'))
def citation_range_updater(citation_slider_value):
    print('citation_range_updater')
    return "Citações entre %d e %d" % (int(citation_slider_value[0]), int(citation_slider_value[1]))


if __name__ == '__main__':
    read_csv('db/db.csv')
    app.layout = main_layout()
    app.run_server(debug=True)
