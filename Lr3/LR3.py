import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State

# Reading the csv file.
data = pd.read_csv("indexData.csv")
# Manipulating the date.
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)
# Initialising application.
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Stock Exchange Analytics", ),
        html.P(
            children="Analyzing day wise opening and closing prices of indexes.",
        ),
        html.Div(
            children=[
                html.Div(
                    children="Date Range",
                    className="menu-title"
                ),
                dcc.DatePickerRange(
                    id="date-range",
                    min_date_allowed=data.Date.min().date(),
                    max_date_allowed=data.Date.max().date(),
                    start_date=data.Date.min().date(),
                    end_date=data.Date.max().date(),
                ),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="open-price-chart", config={"displayModeBar": False},
                        figure={"data": [{
                            "x": data["Date"],
                            "y": data["Open"],
                            "type": "lines",
                        }, ],
                            "layout": {"title": "Day-wise opening prices of indexes"},
                        }
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="close-price-chart", config={"displayModeBar": False},
                        figure={"data": [{
                            "x": data["Date"],
                            "y": data["Close"],
                            "type": "lines",
                        }, ],
                            "layout": {"title": "Day-wise opening prices of indexes"},
                        }
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [
        Output("open-price-chart", "figure"),
        Output("close-price-chart", "figure")
    ],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(start_date, end_date):
    mask = (
            (data.Date >= start_date)
            & (data.Date <= end_date)
    )

    filtered_data = data.loc[mask, :]
    open_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Open"],
                "type": "lines",
                "hovertemplate": "$ % {y: .2f}",
            },
        ],
        "layout": {
            "title": {
                "text": "Opening Price of Indexes",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    close_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Close"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Closing Price of indexes.",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return open_price_chart_figure, close_price_chart_figure


if __name__ == '__main__':
    app.run_server(debug=True)
