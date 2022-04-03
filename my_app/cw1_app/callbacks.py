import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, Input, Output
from dash import html
import my_app.cw1_app.layout as lt


def register_callbacks(dash_app):
    @dash_app.callback(Output("stats-card", "children"),
                       Output("output chart", "figure"),
                       [Input("dropdown", "value")])
    def update_chart(player_name):
        dff = lt.df_players[(lt.df_players['Name'] == player_name)]
        avg_row = {'Name': 'Players average', 'Seconds added': lt.players_mean, 'Comparison': 'Players average'}
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
    @dash_app.callback(Output('tabs-content-tournaments-table', 'children'),
                       Input('tabs-tournaments-table', 'value'))
    def render_content(tab_tournaments):
        if tab_tournaments == 'tab-1-tournaments-table':
            return html.Div([
                html.H3('Fastest tournaments table'),
                dcc.Graph(
                    id='tournaments-1-tabs',
                    figure=lt.create_table(lt.df_events, 0, 10)
                )
            ])

        elif tab_tournaments == 'tab-2-tournaments-table':
            return html.Div([
                html.H3('Slowest tournaments table'),
                dcc.Graph(
                    id='tournaments-2-tabs',
                    figure=lt.create_table(lt.df_events, 195, 205)
                )
            ])

    # To create interactivity of the second tab
    @dash_app.callback(Output('tabs-content-players-table', 'children'),
                       Input('tabs-players-table', 'value'))
    def render_content(tab_players):
        if tab_players == 'tab-1-players-table':
            return html.Div([
                html.H3('Fastest players table'),
                dcc.Graph(
                    id='players-1-tabs',
                    figure=lt.create_table(lt.df_for_table, 0, 10)
                )
            ])

        elif tab_players == 'tab-2-players-table':
            return html.Div([
                html.H3('Slowest players table'),
                dcc.Graph(
                    id='players-2-tabs',
                    figure=lt.create_table(lt.df_for_table, 195, 205)
                )
            ])
