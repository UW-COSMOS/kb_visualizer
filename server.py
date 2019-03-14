import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2, psycopg2.extras
from psycopg2.extensions import AsIs

import json
import flask
import glob
import os

conn = psycopg2.connect("postgres://postgres:@localhost:54321/cosmos_figs")
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

cur.execute("SELECT docid FROM docids;")
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
    """
    TODO: Docstring for build_row.

    Args:
        row (TODO): TODO

    Returns: TODO

    """
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
#        print(cur.mogrify("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d'", {"docid" : AsIs(docid), "btype" : AsIs(btype)}))
        cur.execute("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' ", {"docid" : AsIs(docid), "btype" : AsIs(btype)})
    else:
#        print(cur.mogrify("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' AND target_unicode ilike '%%%%%(search_term)s%%%%'", {"docid" : AsIs(docid), "btype" : AsIs(btype), "search_term" : AsIs(search_term)}))
        cur.execute("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' AND target_unicode ilike '%%%%%(search_term)s%%%%'", {"docid" : AsIs(docid), "btype" : AsIs(btype), "search_term" : AsIs(search_term)})
    headers = ["target_img_path", "target_unicode", "assoc_img_path", "assoc_unicode"]

    table = html.Table(
            [html.Tr([html.Th(i, style={"width" : "25%"}) for i in headers])] +

            [html.Tr(build_row(row, headers)) for row in cur.fetchall()],
            style={'border':'1px solid black', 'font-size':'0.8rem', 'border-color' : 'black'}

            )
    return table


    return 'You\'ve entered "{}"'.format((docid, btype, search_term))

#@app.callback(
#    dash.dependencies.Output('datatable-output', 'children'),
#    [dash.dependencies.Input('datatable', 'rows')])
#def update_output(rows):
#    return html.Pre(
#        json.dumps(rows, indent=2)
#    )

#@app.callback(
#    dash.dependencies.Output('target_image', 'src'),
#    [dash.dependencies.Input('docid-dropdown', 'value'),
#        dash.dependencies.Input('type-dropdown', 'value'),
#        dash.dependencies.Input('search-term', 'value'),
#        ])
#def update_image_src(docid, btype, search_term):
#    print(docid, btype)
#    docid = docid[0]
#    btype = btype
#    # output of this gets fed into the IMG tag above ^
#    if search_term == '':
#        print(cur.mogrify("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype)}))
#        cur.execute("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype)})
#    else:
#        print(cur.mogrify("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' AND target_unicode ilike '%%%%%(search_term)s%%%%' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype), "search_term" : AsIs(search_term)}))
#        cur.execute("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' AND target_unicode ilike '%%%%%(search_term)s%%%%' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype), "search_term" : AsIs(search_term)})
#    hit = cur.fetchone()
#    if hit is None:
#        print("No results...")
#        return ''
#    else:
#        print(static_image_route + hit["target_img_path"])
#        return static_image_route + hit["target_img_path"]

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
    if docid=="ALL":
        docid=".*"
    else:
        docid = docid[0]
    cur.execute("SELECT DISTINCT substring(target_img_path, '^(?:img/){1}(?:%(docid)s)(?:_input.pdf).*\/(.*[^\d])(:?\d+.png)$') AS type FROM things ORDER BY type ASC", {"docid" : AsIs(docid)})
    tmp = [{'label' : i['type'], 'value' : i['type']} for i in cur.fetchall() if i['type'] is not None]
    return tmp

@app.server.route('/images/<path:image_path>'.format(static_image_route))
def serve_image(image_path):
    print("Serving %s" % image_path)
#    image_name = '{}.png'.format(image_path)
    image_name = '{}'.format(image_path)
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)