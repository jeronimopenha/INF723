from dash import html, dcc


def main_layout() -> html.Div:
    return html.Div([
        html.H1('INF 723 - Visor', style={'text-align': 'center'}),
        dcc.Location(id='url', refresh=False),
        dcc.Link('Open data base file', href='/open_database_file',
                 style={'margin-left': '15px', 'text-align': 'right'}),
        html.Br(),
        dcc.Link(' About', href='/about', style={'margin-left': '15px'}),

        # content will be rendered in this element
        html.Div(id='page-content'),
    ])


def about_layout() -> html.Div:
    return html.Div([
        html.H2(f'About'),
        html.P("This is a practical work created as a fundamental \
                    part of evaluation for the discipline for the \
                    discipline Data Visualization of the strictu sensu \
                    postgraduate course in Computer Science at the \
                    Universidade Federal de Viçosa."),
        html.H3('Teacher:'),
        html.P('Sabrina Silveira'),
        html.H3('Students:'),
        html.P('Cleiton Monteiro - ES89321'),
        html.P('Jeronimo Costa Penha - ES91669'),
    ])


def err_layout() -> html.Div:
    return html.Div([
        html.H3(f'ERROR - PAGE NOT FOUND')
    ])

def open_database_layout()->html.Div:
    return html.Div([
        html.H2(f'Open File:'),
        #html.P('Choose a .csv file, drag and drop it below or click to open the file upload window:'),
        dcc.Upload(
            id="upload_db",
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
    ])