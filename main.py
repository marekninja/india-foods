# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import copy

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import math
from collections import Counter

import india as ind
import json

with open('data/india_state.json') as f:
    counties = json.load(f)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, './assets/base.css'])
server = app.server
app.title = "Indi-foods!"

india = ind.get_data()
slider_min = math.floor(min(ind.get_preparation()) / 10) * 10
slider_max = math.ceil(max(ind.get_preparation()) / 10) * 10

app.layout = \
    html.Div(children=[
        dbc.Row([
            dbc.Col([
                html.H1(children="Indi foods!"),
            ], align="start"),
            dbc.Col([
                dbc.Row([
                    dbc.Col(["Get in the mood!"], width="auto"),
                    dbc.Col([html.Audio(id='music',
                                        children="Follow This River to the Sun by Siddhartha Corsus",
                                        src='https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/eETgznrHdYL82xqxybrvt5QPvR5gGWD4igpk2br4.mp3',
                                        loop=True,
                                        controls=True,
                                        autoPlay=False), ], width="auto"),
                ], align="center", justify="center", no_gutters=True)

            ], align="end"),

        ], no_gutters=True, ),
        dbc.Row([
            dbc.Col([html.H2("What will you cook today?")]),
        ]),
        dbc.Row([
            dbc.Col([
                html.H4('1. What is in your fridge?'),

                dcc.Dropdown(
                    id='ingredients-chosen',
                    options=[{'label': ing, 'value': ''.join(ing.split())} for ing in
                             ind.get_ingredients()],
                    multi=True,
                    searchable=True,
                    placeholder="Select owned ingredients",
                    style={"overflowY": "visible"},
                    value=[]),
            ], width=True),
            dbc.Col([
                html.H4('2. How much time do you have?'),
                dcc.Slider(
                    id='prep-slider',
                    min=slider_min,
                    max=slider_max,
                    tooltip={'placement': 'top'},
                    marks={
                        slider_min: '{} minutes'.format(slider_min),
                        slider_max: '{} minutes'.format(slider_max)
                    },
                    drag_value=50,
                    value=50)
            ], width=True)

        ]),
        dbc.Row([
            dbc.Col([
                html.H4("3. Which state will it be?"),
                dcc.Graph(id="choropleth"),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.H4("4. Which flavor do you like?"),
                dcc.Graph(id="pie-chart"),
            ]),
            dbc.Col([
                html.H4("5. Which course do you want?"),
                dcc.Graph(id="hist-stacked")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H4("6. Choose and cook!"),
                dash_table.DataTable(
                    id='table',
                    page_current=0,
                    page_size=15,
                    page_action='custom',
                    style_as_list_view=True,
                )
            ])
        ], align="center"),
        dbc.Row([
            dbc.Col([
                html.A(
                    dbc.Button("Reset all", color="warning", className="mr-1"),
                    href='/'),

            ])
        ]),
        dbc.Row([
            dbc.Col([
                "This app is made as visualization of Kaggle ",
                html.A(['dataset'], href="https://www.kaggle.com/nehaprabhavalkar/indian-food-101"),
                ". Dataset was created by ",
                html.A(['Neha Prabhavalkar'], href="https://www.kaggle.com/nehaprabhavalkar/"),
                "."
            ],width="auto"),
        ], justify="center"),
        dbc.Row([
            dbc.Col([
                "Music is by ",
                html.A(['Siddhartha Corsus'], href="https://freemusicarchive.org/music/Siddhartha"),
                " and song name is  ",
                html.A(['Follow This River to the Sun'], href="https://freemusicarchive.org/music/Siddhartha/mystic-gate-songs-for-the-hidden-peak/follow-this-river-to-the-sun"),
                "."
            ],width="auto"),
        ], justify="center"),

        html.Div([
            html.Div([
                "Created with: ",
                html.A([
                        html.Img(src="/assets/images/logo-plotly.png")
                    ], href="https://plotly.com", className="logo-link"),
                html.Img(src="/assets/images/logo-seperator.png"),
                html.A([
                        html.Img(src="/assets/images/logo-dash.png")
                    ], className="logo-link", href="https://dash.plotly.com/"),
            ], className='logo'),
            html.Div([
                "© Marek Petrovič 2021"
            ]),
            html.Div([
                html.A([
                    html.Img(src="./assets/images/github.svg", className="svg")
                ], href="https://github.com/marekninja", className="logo-link"),
            ], className="logo"),
            html.Div([
                html.A([
                    html.Img(src="./assets/images/linked.svg", className="svg")
                ], href="https://www.linkedin.com/in/marek-petrovic-b9623b1b1/", className="logo-link"),
            ], className="logo")
        ], className="footer"),


        html.Div(id='filtered-by-ingredients', style={'display': 'none'}),
        html.Div(id='filtered-by-state', style={'display': 'none'}),
        html.Div(id='filtered-by-flavor', style={'display': 'none'}),
    ], style={'maxWidth': '1200px',
              'margin': 'auto', 'padding': '1%'}, id='app_content')


@app.callback(
    [Output("choropleth", "figure"),
     Output("filtered-by-ingredients", "children")],
    [Input('ingredients-chosen', 'value'),
     Input('prep-slider', 'value')])
def display_choropleth(chosen, prep_time):
    india_c = copy.deepcopy(india)

    if chosen == None:
        chosen = []

    if prep_time < min(india_c.prep_time):
        prep_time = min(india_c.prep_time)

    india_c['ing2'] = india_c.ingredients
    l = [list(map(str.lstrip, i.split(','))) for i in india_c.ing2]
    india_c.ing2 = [list(filter(lambda x: x not in chosen, i)) for i in l]
    india_c['score'] = [len(i) for i in india_c.ing2]

    # if len(chosen) > 0:
    #     india_c = india_c[india_c.score < 5]

    india_c = india_c[india_c.prep_time <= prep_time]

    india_c = india_c.sort_values(by='score', ascending=True)

    filtered = india_c.drop(['ing2', 'score'], axis=1).to_json()

    print('CHORO update by chosen:', chosen, ' prep:', prep_time)
    # print("chosen",chosen," prepare",prep_time)
    # print("filtered", filtered)

    counts = Counter(india_c.state)
    print(counts)
    # count as percent of total
    top = max(counts.values()) if len(counts.values()) > 0 else 0

    # print(counts)

    data = pd.DataFrame({'state': list(counts), 'recipes': counts.values()})

    fig = px.choropleth_mapbox(
        data,
        geojson=counties,
        color='recipes',
        locations="state",
        featureidkey="properties.NAME_1",
        center={"lat": 22.993413890664062, "lon": 79.77800747040892},
        range_color=[0, top],
        zoom=3
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_accesstoken='pk.eyJ1IjoibWFyZWtuaW5qYSIsImEiOiJja2s3M3RrZjEwYTc0MnBueGRsZHR5YnJ6In0.JloZ4M77Mqh1AayrYYDkjg')
    return fig, filtered


@app.callback(
    [Output("pie-chart", "figure"),
     Output('filtered-by-state', "children")],
    [Input('choropleth', 'clickData'),
     Input('filtered-by-ingredients', 'children')]
)
def generate_pie_hist(clickData, ingredients):
    data = ""
    # print("ingredients", ingredients)
    if ingredients == None:
        data = india
    else:
        data = pd.read_json(ingredients)

    if clickData != None:
        state = clickData["points"][0]['location']
        data = data[data.state == state]

    by_state = data
    print('PIE update by state:', None if clickData == None else clickData["points"][0]['location'])
    # print("by_state",by_state)
    # print(data.columns)

    counts = Counter(data.flavor_profile)
    pie_data = pd.DataFrame({'flavors': list(counts), 'count': counts.values()})

    # title = "4. Which flavor you like?
    pie = px.pie(pie_data, values='count', names='flavors')

    return pie, by_state.to_json()


@app.callback(
    [Output('hist-stacked', 'figure'),
     Output('filtered-by-flavor', 'children')],
    [Input('filtered-by-state', "children"),
     Input('pie-chart', 'clickData')]
)
def generate_hist(by_state, clicked):
    data = ""
    if by_state == None:
        data = india
    else:
        data = pd.read_json(by_state)

    if clicked != None:
        data = data[data.flavor_profile == clicked['points'][0]['label']]

    by_flavor = data.to_json()

    hist = go.Figure()
    for name, group in data.groupby(by='course'):
        his = go.Histogram(x=group.cook_time,
                           name=name)
        hist.add_trace(his)

    # Overlay both histograms
    # title="5. Which course you want?",
    hist.update_layout(barmode='overlay',
                       xaxis_title="Time to cook",
                       yaxis_title="Recipes", )
    # Reduce opacity to see both histograms
    hist.update_traces(opacity=0.75)
    return hist, by_flavor


@app.callback(
    [Output("table", "columns"),
     Output("table", "data"),
     Output("table", "style_cell_conditional")],
    [Input('hist-stacked', 'clickData'),
     Input('filtered-by-flavor', 'children'),
     Input('table', "page_current"),
     Input('table', "page_size")],
    State('hist-stacked', 'figure'),
)
def generate_table(course, by_state, page_current, page_size, course_figure):
    data = ""

    if by_state == None:
        data = india
    else:
        data = pd.read_json(by_state)

    print(json.dumps(course))

    if course != None:
        curve_number = course['points'][0]['curveNumber']
        trace_name = course_figure['data'][curve_number]['name']
        data = data[data.course == trace_name]

    # data = data.sort_values(by=['ingredients'], ascending=True, )

    # data = india
    columns = [{"name": i, "id": i} for i in data.columns]
    table_data = data.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records')

    style_cell_conditional = [
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['name', 'ingredients']
    ]

    return columns, table_data, style_cell_conditional


if __name__ == '__main__':
    app.run_server(debug=False)
