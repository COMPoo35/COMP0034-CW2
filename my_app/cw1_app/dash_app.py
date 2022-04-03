import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from dash import dcc, Input, Output
from dash import html

# external_stylesheets = [dbc.themes.MINTY]
# Create a Dash app that will be configured to display the chart
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ])
# Change the app name
app.title = 'Tennis Match Analysis'

# To read .csv file from prepared dataset.
df_big_four = pd.read_csv('Prepared data set/Big Four time.csv')
df_events = pd.read_csv('Prepared data set/event time.csv')
df_players = pd.read_csv('Prepared data set/player time.csv')
df_for_table = df_players.drop(['Label'], axis=1)
players_mean = df_players['Seconds added'].mean()

# Use Plotly Express to create charts
fig_big_four = px.bar(df_big_four, x="Player-The Big Four", y="Time difference (sec)", color="Comparison",
                      barmode="group")
fig_big_four.update_layout(title="Time before next point compared with \
players average at 2015 French Open", title_font_size=18)

fig_surface = px.box(df_events, x="Surface", y="Seconds added")
fig_surface.update_layout(title="Effects of surface on seconds added per point", title_font_size=18)

fig_players = px.box(df_players, x='Seconds added', y='Label')
fig_players.update_layout(title="Overall statistics of seconds added of 218 players", title_font_size=18)


# A function to create table from dataset
def create_table(dataset, range1, range2):
    fig = ff.create_table(dataset[range1:range2])
    fig.layout.width = 800
    return fig


app.layout = dbc.Container(fluid=False, children=[
    html.H1(children='Why Some Tennis Matches Take Forever'),
    html.Br(),
    html.H4('Surfaces Speeds'),
    html.H6("--Average time added per point in men's tennis"),
    html.Br(),

    # Create two tabs to display tables
    dcc.Tabs(id="tabs-tournaments-table", value='tab-1-tournaments-table', children=[
        dcc.Tab(label='Table 1', value='tab-1-tournaments-table'),
        dcc.Tab(label='Table 2', value='tab-2-tournaments-table'),
    ], style={'width': '60%'}),
    html.Div(id='tabs-content-tournaments-table'),

    html.Br(),
    html.H4('Overall effect of surfaces on match time'),
    dcc.Graph(
        id='Surface time graph',
        figure=fig_surface
    ),
    html.H4('Player Speeds'),
    html.H6("--Average time added per point in men's tennis"),
    html.Br(),

    # Create two tabs to display tables
    dcc.Tabs(id="tabs-players-table", value='tab-1-players-table', children=[
        dcc.Tab(label='Table 1', value='tab-1-players-table'),
        dcc.Tab(label='Table 2', value='tab-2-players-table'),
    ], style={'width': '60%'}),
    html.Div(id='tabs-content-players-table'),

    html.Br(),
    html.H4('Players have different speeds'),

    html.P(children='''
    Nine-time French Open champ Rafael Nadal is one of the slowest players of the last 25 years. 
    Roger Federer is faster than average. Novak Djokovic is slower than average — but has gotten faster. 
    Andy Murray, on the other hand, has slowed down.
    The following chart displays the data for the Big Four serving at 2015 French Open.
'''),
    html.Br(),
    dcc.Graph(
        id='Big Four time graph',
        figure=fig_big_four
    ),

    html.Br(),
    dcc.Graph(
        id='Players box graph',
        figure=fig_players
    ),

    # First row
    dbc.Row([
        dbc.Col(html.H5("Select a player to display data"), width=5),
        dbc.Col(html.H5("Comparison between selected player and the average")),
    ]),

    # Second row
    dbc.Row([
        # This is for the player selector and the statistics panel.
        dbc.Col(width={'size': 3}, children=[
            dcc.Dropdown(id='dropdown', options=[
                {'label': x, 'value': x} for x in df_players['Name']
            ]),
            # Div that will later contain a bootstrap card format showing the stats.
            html.Br(),
            html.Div(id="stats-card")
        ]),
        # Add the second column. This is for the comparison figure.
        dbc.Col(
            dcc.Graph(
                id='output chart',
                figure={}
            ),
            width={'size': 'auto', 'offset': 2}
        )
    ]),
])


# To create interactivity of card and comparison chart
@app.callback(Output("stats-card", "children"),
              Output("output chart", "figure"),
              [Input("dropdown", "value")])
def update_chart(player_name):
    dff = df_players[(df_players['Name'] == player_name)]
    avg_row = {'Name': 'Players average', 'Seconds added': players_mean, 'Comparison': 'Players average'}
    dff.insert(2, 'Comparison', 'Selected player')
    # Add a new row to dff for comparison
    df_for_comparison = dff.append(avg_row, ignore_index=True)
    fig_selected_player = px.bar(df_for_comparison, x='Name', y='Seconds added', color="Comparison",
                                 barmode="group")
    # Create card to display player stats
    card = dbc.Card(className="bg-dark text-light", children=[
        dbc.CardBody([
            html.H4(player_name, id="player-name", className="card-title"),
            html.Br(),
            html.H6("Seconds added per point:", className="card-title"),
            html.H4(dff['Seconds added']),
        ])
    ])

    return card, fig_selected_player


# To create interactivity of the first tab
@app.callback(Output('tabs-content-tournaments-table', 'children'),
              Input('tabs-tournaments-table', 'value'))
def render_content(tab_tournaments):
    if tab_tournaments == 'tab-1-tournaments-table':
        return html.Div([
            html.H3('Fastest tournaments table'),
            dcc.Graph(
                id='tournaments-1-tabs',
                figure=create_table(df_events, 0, 10)
            )
        ])

    elif tab_tournaments == 'tab-2-tournaments-table':
        return html.Div([
            html.H3('Slowest tournaments table'),
            dcc.Graph(
                id='tournaments-2-tabs',
                figure=create_table(df_events, 195, 205)
            )
        ])


# To create interactivity of the second tab
@app.callback(Output('tabs-content-players-table', 'children'),
              Input('tabs-players-table', 'value'))
def render_content(tab_players):
    if tab_players == 'tab-1-players-table':
        return html.Div([
            html.H3('Fastest players table'),
            dcc.Graph(
                id='players-1-tabs',
                figure=create_table(df_for_table, 0, 10)
            )
        ])

    elif tab_players == 'tab-2-players-table':
        return html.Div([
            html.H3('Slowest players table'),
            dcc.Graph(
                id='players-2-tabs',
                figure=create_table(df_for_table, 195, 205)
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
