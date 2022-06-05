#from xml.etree.ElementInclude import include
import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from src.layouts import *

UPLOAD_DIRECTORY = "../db"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# main header layout
app.layout = main_layout()


@app.callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        return about_layout()
    elif pathname == '/open_database_file':
        return open_database_layout()
    else:
        return err_layout()


@app.callback(Output('output-data-upload', 'children'),
              Input('upload_db', 'contents'),
              State('upload_db', 'filename'),
              State('upload_db', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("estou aqui")
    '''if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    '''


if __name__ == '__main__':
    app.run_server(debug=True)
