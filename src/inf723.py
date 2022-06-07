import base64
import io
from os import read
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# layouts


def main_layout() -> html.Div:
    return html.Div([
        html.H1('INF 723 - Visor', style={'text-align': 'center'}),
        html.P("AQUI SERÁ PRECISO COLOCAR O QUE É A FERRAMENTA E PRA QUE ELA SERVE"),
        html.P("PRECISAMOS VER UMA FORMA DE APRESENTAR A FERRAMENTA E OS GRÁFICOS A SEREM COLOCADOS"),
        html.P("PRECISAMOS DEFINIR O LAYOUT DE ACORDO COM O QUE VC ESTUDOU EM GESTALT E ALGUMA COISA DE VAZIO LÁ HEHEH"),
        html.P("EU OLHAREI A QUESTÃO DAS CORES, MAS ACHO QUE O PLOTLY JÁ ESCOLHE AS CORES DE ACORDO COM O QUE VI NO SITE"),
        html.P("NESSE MOMENTO EU ACHO QUE É MAIS IMPORTANTE A GENTE DAR ATENÇÃO AOS PONTOS DA MATÉRIA EM RELAÇÃO A VISUALIZAÇÃO DO QUE EM RELAÇÃO A QUANTIDADE DE GRÁFICOS EM SI"),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.H3(f'AQUI COLOCAREMOS OS AUTORES DA FERRAMENTA'),
        html.P("This is a practical work created as a fundamental \
                    part of evaluation for the discipline for the \
                    discipline Data Visualization of the strictu sensu \
                    postgraduate course in Computer Science at the \
                    Universidade Federal de Viçosa."),
        html.H3('Professor:'),
        html.P('Sabrina Silveira'),
        html.H3('Students:'),
        html.P('Cleiton Monteiro - ES89321'),
        html.P('Jeronimo Costa Penha - ES91669'),
    ])


def about_layout() -> html.Div:
    return html.Div([
        html.H2(f'About'),
        html.P("This is a practical work created as a fundamental \
                    part of evaluation for the discipline for the \
                    discipline Data Visualization of the strictu sensu \
                    postgraduate course in Computer Science at the \
                    Universidade Federal de Viçosa."),
        html.H3('Professor:'),
        html.P('Sabrina Silveira'),
        html.H3('Students:'),
        html.P('Cleiton Monteiro - ES89321'),
        html.P('Jeronimo Costa Penha - ES91669'),
    ])


def err_layout() -> html.Div:
    return html.Div([
        #html.H3(f'ERROR - PAGE NOT FOUND')
    ])


def analysis_layout() -> html.Div:
    return html.Div([
        html.H2(f'Open File:'),
        html.P(
            'Choose the data base file ".csv", and drag and drop it below or click in the box below to open the file upload window:'),
        dcc.Upload(
            id="upload-db",
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.Div(id='output-data-upload'),
    ])
# ---------------

# callbacks


@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def update_page_content_div(input_value):
    if input_value == "/about":
        print("about page called")
        return about_layout()
    elif input_value == "/analysis_layout":
        print("open database file page called")
        return analysis_layout()
    else:
        return err_layout()


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-db', 'contents'),
              State('upload-db', 'filename'),
              State('upload-db', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        print("upload data_base handler")
        return read_csv(list_of_contents, list_of_names, list_of_dates)
    return None
# ---------------

# other functions


def read_csv(contents, filename, date):
    print("csv reader")
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            read = True
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            read = True
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    fig = px.sunburst(df, path=['qualis', 'publication', 'year', 'name'])

    return html.Div([
        dcc.Graph(style={'height': '1024px'}, figure=fig)
    ])

# ---------------


app.layout = main_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
