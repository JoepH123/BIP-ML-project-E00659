import base64
import io
import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc


#Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = "Exemption code predictor"

tab1_content = html.Div(children=[
    html.Br(),
    dbc.Row(
        dbc.Col(
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files (.csv or .xlsx)')
                ]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',
                    'textAlign': 'center', 'margin': '10px', 'color': '#e3e3e3', 'fontWeight': 'bold'  # 'color': '#888'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            width=4
        ),
        justify="center"
    ),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dash_table.DataTable(
                    id='output-data-table',
                    page_size=10,  # Display 10 rows per page
                    style_table={'overflowY': 'hidden', 'borderRadius': '15px', 'boxShadow': '0 2px 2px 0 rgba(0,0,0,0.2)'},
                    style_cell={'padding': '10px', 'textAlign': 'left', 'border': 'none', 'color': "#444444"},
                    style_header={
                        'backgroundColor': 'rgb(0, 43, 54, 1)',
                        'fontWeight': 'bold',
                        'borderTopLeftRadius': '15px',
                        'borderTopRightRadius': '15px',
                        'color': '#e3e3e3',
                        'padding': '10px',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },             
                        {
                            "if": {"state": "selected"}, # 'active' | 'selected'
                            "backgroundColor": None, 
                            "border": "3px solid #b58900",
                        },
                    ],
                ),
                body=True,  # This ensures that the card body styling is applied
                # style={'borderRadius': '15px', 'boxShadow': '0 2px 2px 0 rgba(0,0,0,0.2)', 'marginTop': '20px'}
            ),
            width=10
        ),
        justify="center"
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id='clicked-row', style={"textAlign": "center", "color": "#e3e3e3"}),
            width=12
        ),
        justify="center"
    )
])

tab2_content = html.Div(children=[
    html.Div([
        html.Br(),
        dbc.InputGroup(
            [dbc.InputGroupText("@"), dbc.Input(placeholder="Username")],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.Input(placeholder="Recipient's username"),
                dbc.InputGroupText("@example.com"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Total:"),
                dbc.InputGroupText("$"),
                dbc.Input(placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
                dbc.InputGroupText("only"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("With textarea"),
                dbc.Textarea(),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.Select(
                    options=[
                        {"label": "Option 1", "value": 1},
                        {"label": "Option 2", "value": 2},
                    ]
                ),
                dbc.InputGroupText("With select"),
            ]
        ),
    ], style={"width": "60%", "margin": "0 auto"}),
    html.Br(),
    html.Div(
        dbc.Button("Submit"),
        style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"}
    )
])

# Custom layout with dbc components
app.layout = dbc.Container([
    html.Br(),
    html.H1('VAT Exemption Code Predictor', style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#e3e3e3'}),

    # Different tabs approach
    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Tab 1"),
            dbc.Tab(tab2_content, label="Tab 2"),
        ], style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"}
    )

    # Old approach --> only upload file

    # dbc.Row(
    #     dbc.Col(
    #         dcc.Upload(
    #             id='upload-data',
    #             children=html.Div([
    #                 'Drag and Drop or ',
    #                 html.A('Select Files')
    #             ]),
    #             style={
    #                 'width': '100%', 'height': '60px', 'lineHeight': '60px',
    #                 'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',
    #                 'textAlign': 'center', 'margin': '10px', 'color': '#e3e3e3', 'fontWeight': 'bold'  # 'color': '#888'
    #             },
    #             # Allow multiple files to be uploaded
    #             multiple=False
    #         ),
    #         width=4
    #     ),
    #     justify="center"
    # ),
    # dbc.Row(
    #     dbc.Col(
    #         dbc.Card(
    #             dash_table.DataTable(
    #                 id='output-data-table',
    #                 page_size=10,  # Display 10 rows per page
    #                 style_table={'overflowY': 'hidden', 'borderRadius': '15px', 'boxShadow': '0 2px 2px 0 rgba(0,0,0,0.2)'},
    #                 style_cell={'padding': '10px', 'textAlign': 'left', 'border': 'none', 'color': "#444444"},
    #                 style_header={
    #                     'backgroundColor': 'rgb(0, 43, 54, 1)',
    #                     'fontWeight': 'bold',
    #                     'borderTopLeftRadius': '15px',
    #                     'borderTopRightRadius': '15px',
    #                     'color': '#e3e3e3',
    #                     'padding': '10px',
    #                 },
    #                 style_data_conditional=[
    #                     {
    #                         'if': {'row_index': 'odd'},
    #                         'backgroundColor': 'rgb(248, 248, 248)'
    #                     }
    #                 ],
    #             ),
    #             body=True,  # This ensures that the card body styling is applied
    #             style={'borderRadius': '15px', 'boxShadow': '0 2px 2px 0 rgba(0,0,0,0.2)', 'marginTop': '20px'}
    #         ),
    #         width=10
    #     ),
    #     justify="center"
    # ),
    # dbc.Row(
    #     dbc.Col(
    #         html.Div(id='clicked-row', style={"textAlign": "center", "color": "#e3e3e3"}),
    #         width=12
    #     ),
    #     justify="center"
    # )
], fluid=True)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div([
                'Wrong file type inserted.'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(Output('output-data-table', 'data'),
              Output('output-data-table', 'columns'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if not isinstance(df, pd.DataFrame):
            return [], []
        columns = [{'name': i, 'id': i} for i in df.columns]
        data = df.to_dict('records')
        return data, columns
    return [], []

@app.callback(Output('clicked-row', 'children'),
              Input('output-data-table', 'active_cell'),
              State('output-data-table', 'data'))
def display_click_data(active_cell, rows):
    if active_cell and rows:
        col_id = active_cell['column_id']
        row = rows[active_cell['row']]
        return f'You clicked on row {active_cell["row"] + 1}, column {col_id}, which has value: {row[col_id]}'
    return 'Click a row after uploading a file to see details here.'

if __name__ == '__main__':
    app.run_server(debug=True)
