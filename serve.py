import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2, psycopg2.extras
from psycopg2.extensions import AsIs

import flask
import glob
import os

conn = psycopg2.connect("postgres://postgres:@localhost:54321/cosmos_figs")
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

cur.execute("SELECT docid FROM docids;")
docids = cur.fetchall()
cur.execute("SELECT type FROM types;")
types = cur.fetchall()




image_directory = os.getcwd()
list_of_images = [os.path.basename(i["target_img_path"]) for i in cur.fetchall()]
static_image_route = '/dummy/'

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='docid-dropdown',
        options=[{'label': i, 'value': i} for i in docids],
        value = docids[0],
        placeholder="Select a document",
    ),
    dcc.Dropdown(
        id='type-dropdown',
        options=[{'label': i, 'value': i} for i in types],
        placeholder="Select a box type"
    ),
    html.Img(id='target_image')
    ])



@app.callback(
    dash.dependencies.Output('target_image', 'src'),
    [dash.dependencies.Input('docid-dropdown', 'value'),
        dash.dependencies.Input('type-dropdown', 'value')])
def update_image_src(docid, btype):
    print(docid, btype)
    docid = docid[0]
    btype = btype
    # output of this gets fed into the IMG tag above ^
    print(cur.mogrify("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype)}))
    cur.execute("SELECT * FROM things WHERE target_img_path ~ '%(docid)s.*%(btype)s\d' LIMIT 1", {"docid" : AsIs(docid), "btype" : AsIs(btype)})
    hit = cur.fetchone()
    if hit is None:
        print("No results...")
        return ''
    else:
        print(static_image_route + hit["target_img_path"])
        return static_image_route + hit["target_img_path"]


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
    docid = docid[0]
    print(cur.mogrify("SELECT DISTINCT substring(target_img_path, '^(?:img/){1}(?:%(docid)s)(?:_input.pdf).*\/(.*[^\d])(:?\d+.png)$') AS type FROM things", {"docid" : AsIs(docid)}))
    cur.execute("SELECT DISTINCT substring(target_img_path, '^(?:img/){1}(?:%(docid)s)(?:_input.pdf).*\/(.*[^\d])(:?\d+.png)$') AS type FROM things", {"docid" : AsIs(docid)})
    tmp = [{'label' : i['type'], 'value' : i['type']} for i in cur.fetchall() if i['type'] is not None]
    print(tmp)
    return tmp

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
#@app.server.route('{}/<path:image_path>'.format(static_image_route))
@app.server.route('/dummy/<path:image_path>'.format(static_image_route))
def serve_image(image_path):
    print("Serving %s" % image_path)
#    image_name = '{}.png'.format(image_path)
    image_name = '{}'.format(image_path)
#    if image_name not in list_of_images:
#        import pdb; pdb.set_trace()
#        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

@app.server.route('/dummy/<path:subpath>')
def show_subpath_dummy(subpath):
    # show the subpath after /path/
    print("Subpath")
    print(subpath)
    return 'Subpath %s' % subpath
@app.server.route('/static/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    print("Subpath")
    print(subpath)
    return 'Subpath %s' % subpath

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
