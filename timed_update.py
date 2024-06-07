from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from firebase import get_data_from_firebase

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("H2Optimal - Monitoramento em tempo real")),
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div("Quantidade de medições:"), width="auto", align="center"
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="data-points-dropdown",
                        options=[
                            {"label": "100", "value": 100},
                            {"label": "200", "value": 200},
                            {"label": "500", "value": 500},
                        ],
                        value=100,
                        clearable=False,
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="live-graph-calc"), width=4),
                dbc.Col(dcc.Graph(id="live-graph-umidade"), width=4),
                dbc.Col(dcc.Graph(id="live-graph-controle"), width=4),
            ]
        ),
        dcc.Interval(id="interval-component", interval=5 * 1000, n_intervals=0),
    ],
    fluid=True,
)


@app.callback(
    Output("live-graph-calc", "figure"),
    Output("live-graph-umidade", "figure"),
    Output("live-graph-controle", "figure"),
    Input("interval-component", "n_intervals"),
    Input("data-points-dropdown", "value"),
)
def update_graphs(n_intervals, data_points):
    df = get_data_from_firebase()
    if df.empty:
        return {}, {}, {}

    df = df.tail(data_points)

    fig_calc = px.line(df, x=df.index, y="calc", title="Força da bomba")
    fig_calc.update_traces(line=dict(color="#25D366"))
    fig_calc.update_layout(template="plotly_dark")

    fig_umidade = px.line(df, x=df.index, y="umidade", title="Umidade")
    fig_umidade.update_traces(line=dict(color="#25D366"))
    fig_umidade.update_layout(template="plotly_dark")

    fig_controle = px.line(df, x=df.index, y="controle", title="Controle manual")
    fig_controle.update_traces(line=dict(color="#25D366"))
    fig_controle.update_layout(template="plotly_dark")

    return fig_calc, fig_umidade, fig_controle


if __name__ == "__main__":
    app.run_server(debug=True)
