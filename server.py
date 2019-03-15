import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2, psycopg2.extras
import sys
from psycopg2.extensions import AsIs

import json
import flask
import glob
import time
import os
import subprocess

if "PG_CONN_STR" not in os.environ:
    print("Please provide a PG_CONN_STR!")
    sys.exit(1)
if "PG_EQUATION_SCHEMA" in os.environ:
    schema = os.environ["PG_EQUATION_SCHEMA"]
else:
    schema = "public"

wait = True
n_tries = 0
while wait and n_tries < 10:
    try:
        conn = psycopg2.connect(os.environ["PG_CONN_STR"])
        wait = False
    except:
        print("Waiting for db to start up")
        time.sleep(10)

# TODO: maybe don't try to import every time?
subprocess.run(["./setup.sh", schema], env=os.environ)

cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

cur.execute(f"SELECT docid FROM {schema}.docids;")
docids = cur.fetchall()

image_directory = os.getcwd()

static_image_route = '/images/'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='docid-dropdown',
        options=[{"label" : "ALL", "value" : "ALL"}] + [{'label': i, 'value': i} for i in docids] ,
#        options=[{'label': i, 'value': i} for i in docids] ,
#        value = docids[0],
        placeholder="Select a document",
    ),
    dcc.Dropdown(
        id='type-dropdown',
#        options=[{'label': i, 'value': i} for i in types],
        placeholder="Select a box type"
    ),
    dcc.Input(
        id='search-term',
        placeholder='Enter a search string (optional)',
        type='text',
        value=''
    ),
    html.Br(),
    html.Div(id='my-div'),
    ])

app.config['suppress_callback_exceptions']=True

def build_row(row, headers):
    cols = []
    for header in headers:
        try:
            if "img" in header:
                cols.append(html.Td(html.Img(src=static_image_route + row[header], style={"width" : 250}), style={"width" : "25%"}))
            else:
                cols.append(html.Td(row[header], style={"width" : "25%"}))
        except:
            cols.append(html.Td(style={"width" : "25%"}))
    return cols

@app.callback(
    dash.dependencies.Output(component_id='my-div', component_property='children'),
    [dash.dependencies.Input('docid-dropdown', 'value'),
        dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('search-term', 'value')])
def generate_table(docid, btype, search_term):
    if docid == "ALL":
        docid=""
    else:
        docid=docid[0]

    if search_term == '':
#        print(cur.mogrify("SELECT * FROM figures_and_tables WHERE target_img_path ~ '%(docid)s.*%(btype)s\d'", {"docid" : AsIs(docid), "btype" : AsIs(btype)}))
        cur.execute(f"SELECT * FROM %(schema)s.figures_and_tables WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' ", {"docid" : AsIs(docid), "btype" : AsIs(btype)})
    else:
        cur.execute("SELECT * FROM %(schema)s.figures_and_tables WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' AND target_unicode ilike '%%%%%(search_term)s%%%%'", {"schema" : AsIs(schema), "docid" : AsIs(docid), "btype" : AsIs(btype), "search_term" : AsIs(search_term)})
    headers = ["target_img_path", "target_unicode", "assoc_img_path", "assoc_unicode"]

    table = html.Table(
            [html.Tr([html.Th(i, style={"width" : "25%"}) for i in headers])] +

            [html.Tr(build_row(row, headers)) for row in cur.fetchall()],
            style={'border':'1px solid black', 'font-size':'0.8rem', 'border-color' : 'black'}

            )
    return table


    return 'You\'ve entered "{}"'.format((docid, btype, search_term))

@app.callback(
    dash.dependencies.Output('docid-dropdown', 'value'),
    [dash.dependencies.Input('docid-dropdown', 'options')])
def set_docid_value(options):
    print("Setting docid dropdown")
    return options[0]['value']

@app.callback(
    dash.dependencies.Output('type-dropdown', 'value'),
    [dash.dependencies.Input('type-dropdown', 'options')])
def set_type_value(options):
    return options[0]['value']

@app.callback(
    dash.dependencies.Output('type-dropdown', 'options'),
    [dash.dependencies.Input('docid-dropdown', 'value')])
def update_types(docid):
    print(f"Getting types for docid {docid}")
    if docid=="ALL":
        docid=".*"
    else:
        docid = docid[0]
    print(cur.mogrify("SELECT DISTINCT substring(target_img_path, '^(?:img/){1}(?:%(docid)s)(?:_input.pdf).*\/(.*[^\d])(:?\d+.png)$') AS type FROM %(schema)s.figures_and_tables ORDER BY type ASC", {"schema" : AsIs(schema), "docid" : AsIs(docid)}))
    cur.execute("SELECT DISTINCT substring(target_img_path, '^(?:img/){1}(?:%(docid)s)(?:_input.pdf).*\/(.*[^\d])(:?\d+.png)$') AS type FROM %(schema)s.figures_and_tables ORDER BY type ASC", {"schema" : AsIs(schema), "docid" : AsIs(docid)})
    tmp = [{'label' : i['type'], 'value' : i['type']} for i in cur.fetchall() if i['type'] is not None]
    return tmp

@app.server.route('/images/<path:image_path>'.format(static_image_route))
def serve_image(image_path):
#    image_name = '{}.png'.format(image_path)
    image_name = '{}'.format(image_path)
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051)
