import base64
import io
import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    dash_table.DataTable(
        id='output-data-table',
        page_size=10,  # Display 10 rows per page
        style_table={'height': '300px', 'overflowY': 'auto'},
    ),
    html.Div(id='clicked-row')
])

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
