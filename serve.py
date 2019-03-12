import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2, psycopg2.extras

import flask
import glob
import os

conn = psycopg2.connect("postgres://postgres:@localhost:54321/cosmos_figs")
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

cur.execute("SELECT target_img_path FROM figures WHERE target_img_path~'Figure\d.png';")
image_directory = os.getcwd() + "/img/57ede925cf58f16acb2290ac_input.pdf_6/"
list_of_images = [os.path.basename(i["target_img_path"]) for i in cur.fetchall()]
static_image_route = '/static/'
print(image_directory)
print(list_of_images[0])

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images],
        value=list_of_images[0]
    ),
    html.Img(id='image')
])

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    return static_image_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>'.format(static_image_route))
def serve_image(image_path):
    print("Serving %s" % image_path)
#    image_name = '{}.png'.format(image_path)
    image_name = '{}'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
