import flask
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html

from data import frames
from data.frames import Frame

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

app.title = 'Text framing'

# HEADER
# ======

header = dbc.NavbarSimple(
    dbc.NavItem(dbc.NavLink(
        "Source", href="https://github.com/lilyminium/text-framing")),
    # dbc.DropdownMenu(
    #     children=[
    #         dbc.DropdownMenuItem("More pages", header=True),
    #         dbc.DropdownMenuItem("Page 2", href="#"),
    #         dbc.DropdownMenuItem("Page 3", href="#"),
    #     ],
    #     nav=True,
    #     in_navbar=True,
    #     label="More",
    # ),
    brand="Generating text headers",
    brand_href="#",
    color="primary",
    dark=True
)


# COMPONENTS
# ==========

# Your components go here.

explanation = dcc.Markdown("""\
Generate framed, centered text headers.

Select some default options and edit the frame options,
then click Generate text to get your frame.
""", style={'margin': '20px'})

text = dbc.FormGroup([
    dbc.Label('Text for framing'),
    dbc.Textarea(id='header-text',
                 placeholder='heading',
                 value='')
])

hspace = dbc.FormGroup([
    dbc.Label('# horizontal spaces', width=6),
    dbc.Col(dbc.Input(id='hspace',
                      type='number',
                      value=8,
                      min=0, max=100, step=1),
            width=4)

], row=True)

vspace = dbc.FormGroup([
    dbc.Label('# empty rows', width=6),
    dbc.Col(dbc.Input(id='vspace',
                      type='number',
                      value=1,
                      min=0, max=100, step=1),
            width=4)

], row=True)

frame_options = [{'label': str(k).split('\n')[0], 'value': i}
                 for i, k in enumerate(frames)]

frame_radio = dbc.FormGroup([
    dbc.Label('Frame', width=2, html_for='frame-radio'),
    dbc.Col(dcc.Dropdown(
        id='frame-radio',
        options=frame_options,
        # style={'width': '100%'},
        value=0,
    ), width=8),
], row=True)

frame_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Label('Top left corner'),
                dbc.Input(id='tl', type='text')
            ]),
            dbc.Col([
                dbc.Label('Top center'),
                dbc.Input(id='tm', type='text')
            ]),
            dbc.Col([
                dbc.Label('Top right corner'),
                dbc.Input(id='tr', type='text')
            ]),
        ], align='center'),

        dbc.Row([
            dbc.Col([
                dbc.Label('Bottom left corner'),
                dbc.Input(id='bl', type='text')
            ]),
            dbc.Col([
                dbc.Label('Bottom center'),
                dbc.Input(id='bm', type='text')
            ]),
            dbc.Col([
                dbc.Label('Bottom right corner'),
                dbc.Input(id='br', type='text')
            ]),
        ], align='center'),
        dbc.Row([
            dbc.Col([
                dbc.Label('Horizontal divider (left)'),
                dbc.Input(id='lhd', type='text')
            ]),
            dbc.Col([
                dbc.Label('Horizontal divider (right)'),
                dbc.Input(id='rhd', type='text')
            ]),
            dbc.Col([
                dbc.Label('Vertical divider'),
                dbc.Input(id='vd', type='text')
            ])
        ], align='center'),
    ]),
], style={'margin': '10px'})

submit = html.Button('Generate text', id='submit', style={'margin': '10px'})

output = dbc.FormGroup([
    dbc.Textarea(id='output',
                 rows=5,
                 style={'fontFamily': 'monospace'})
])


# APP LAYOUT
# ==========

app.layout = html.Div([
    header,
    explanation,
    dbc.Card([
        dbc.CardBody([
            html.H3('Input'),
            text,
            frame_radio,
            frame_card,
            hspace,
            vspace,
            submit,
        ])
    ], style={'margin': '20px', 'padding': '10px'}),
    dbc.Card([
        html.H3('Output'),
        dbc.CardBody([output])
    ], style={'margin': '20px', 'padding': '10px'}),
], )


# INTERACTION
# ===========

# Your interaction goes here.


@app.callback(
    [Output('tl', 'value'), Output('tm', 'value'), Output('tr', 'value'),
     Output('bl', 'value'), Output('bm', 'value'), Output('br', 'value'),
     Output('vd', 'value'), Output('lhd', 'value'), Output('rhd', 'value')],
    [Input('frame-radio', 'value')]
)
def populate_cells(index):
    f = frames[index]
    return f.tl, f.tm, f.tr, f.bl, f.bm, f.br, f.vd, f.lhd, f.rhd


@app.callback(
    Output('output', 'value'),
    [Input('submit', 'n_clicks')],
    [State('header-text', 'value'),
     State('hspace', 'value'), State('vspace', 'value'),
     State('tl', 'value'), State('tm', 'value'), State('tr', 'value'),
     State('bl', 'value'), State('bm', 'value'), State('br', 'value'),
     State('vd', 'value'), State('lhd', 'value'), State('rhd', 'value')]
)
def generate_text(nclicks, text, nh, nv, *args):
    if not text:
        text = ''
    strings = [x if x else '' for x in args]
    tl, tm, tr, bl, bm, br, vd, lhd, rhd = strings
    f = Frame([[tl, tm, tr], [bl, bm, br]], hd=(lhd, rhd), vd=vd)
    return f.frame_text(text, hspace=nh, vspace=nv)


if __name__ == '__main__':
    app.run_server(debug=True)
