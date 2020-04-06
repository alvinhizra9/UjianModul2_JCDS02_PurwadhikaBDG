import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np 
import plotly.graph_objects as go 
import seaborn as sns
import dash_table
import plotly.express as px


df = pd.read_csv('tsa_claims_dashboard_ujian.csv')

def generate_table(data, nrows=10):
    return dash_table.DataTable(
        id = 'dataTable',
        columns = [{'name' : i,'id' : i} for i in data.columns],
        data = data.to_dict('records'),
        style_table = {'overflowX' : 'scroll'},
        page_action = 'native',
        page_current = 0,
        page_size = nrows
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

app.title = 'Plotly Dashboard'

app.layout = html.Div([html.H1('Ujian Modul 2 Dashboard TSA'),
            html.P('Created by : Alvin Hizra Muhammad'),
            html.Div([html.Div(children = [
            dcc.Tabs(id = 'tabs',children = [
                dcc.Tab(
                    label = 'DataFrame Table', children = [html.H1('DataFrame TSA'),
                    generate_table(df.drop('Unnamed: 0',axis=1))]
                ),
                dcc.Tab(
                    label = 'Bar-Chart',children = [
                    html.Div([
                        html.P('Y1 : '),
                        dcc.Dropdown(
                            id = 'dropdown BarY1 plot',
                            options = [
                                {'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                {'label' : 'Day Differences', 'value' : 'Day Differences'},
                                {'label' : 'Amount Differences', 'value' : 'Amount Differences'}], 
                            value = 'Claim Amount'
                        )],
                        style = {
                            'paddingBottom' : '40px',
                        }
                    ),
                    html.Div([
                        html.P('Y2 : '),
                        dcc.Dropdown(
                            id = 'dropdown BarY2 plot',
                            options = [
                                {'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                {'label' : 'Day Differences', 'value' : 'Day Differences'},
                                {'label' : 'Amount Differences', 'value' : 'Amount Differences'}],
                            value = 'Close Amount'
                        )],
                        style = {
                            'paddingBottom' : '40px',
                        }
                    ),
                    html.Div([
                        html.P('X : '),
                        dcc.Dropdown(
                            id = 'dropdown BarX plot',
                            options = [
                                {'label' : 'Claim Type', 'value' : 'Claim Type'},
                                {'label' : 'Claim Site', 'value' : 'Claim Site'},
                                {'label' : 'Status', 'value' : 'Status'},
                                {'label' : 'Disposition', 'value' : 'Disposition'}],
                            value = 'Claim Type'
                        )],
                        style = {
                            'paddingBottom' : '40px',
                        }
                    ),
                    html.Div([html.P('Bar Chart')],
                    style = {
                                'paddingBottom' : '40px',
                                'text-align' : 'center'
                            }
                    ),
                    dcc.Graph(
                        id = 'Bar Plot Graph',
                        figure = go.Figure(data=[
                                            go.Bar(name = 'Claim Amount',x=df['Claim Type'].unique(), y = list(df[df['Claim Type'] == i]['Claim Amount'].mean() for i in df['Claim Type'].unique())),
                                            go.Bar(name = 'Close Amount',x=df['Claim Type'].unique(), y = list(df[df['Claim Type'] == i]['Close Amount'].mean() for i in df['Claim Type'].unique()))
                                            ]
                                )
                    )
                    ]
                ),
                dcc.Tab(
                    label = 'Scatter-Chart',children = [
                        dcc.Graph(
                            id = 'Scatter Plot Graph',
                            figure = px.scatter(df,
                                                x='Claim Amount',
                                                y='Close Amount',
                                                color = 'Claim Type',
                                                hover_name = 'Status'
                                                ).update_traces(
                                    marker=dict(
                                        size = 10,
                                        line = {
                                            'width' : 0.5,
                                            'color' : 'white'
                                        }
                                    ),selector=dict(mode='markers')
                                ).update_layout(
                                    xaxis={'title' : 'Claim Amount'},
                                    yaxis={'title' : 'Close Amount'},
                                    margin={'l':40,'b':40,'t':10,'r':10}
                                )
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Pie-Chart',children = [
                    html.Div([
                            dcc.Dropdown(
                                id = 'dropdown Pie plot',
                                options = [
                                    {'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                    {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                ], value = 'Claim Amount'
                            )
                            ],style = {
                                'paddingBottom' : '40px',
                            }
                    ),
                    html.Div([
                            html.P('Mean Pie Chart')
                    ],
                    style = {
                                'paddingBottom' : '40px',
                                'text-align' : 'center'
                            }),
                        dcc.Graph(
                            id = 'Pie Plot Graph',
                            figure = px.pie(df,
                                            values = 'Claim Amount',
                                            names='Claim Type'
                                            )
                        )
                    ]
                )
            ],
            style = {
                'fontFamily' : 'system-ui'
            },
            content_style = {
                'fontFamily' : 'Arial',
                'borderBottom' : '1px solid #000000',
                'borderLeft' : '1px solid #000000',
                'borderRight' : '1px solid #000000',
                'padding' : '30px'
            }
)],style = {
        'maxwidth' : '1000px',
        'margin' : '0 auto'}
)])])

@app.callback(
    dash.dependencies.Output('Bar Plot Graph','figure'),
    [dash.dependencies.Input('dropdown BarY1 plot','value'),
    dash.dependencies.Input('dropdown BarY2 plot','value'),
    dash.dependencies.Input('dropdown BarX plot','value'),]
)

def update_Bar_plot(dropdown_BarY1_plot,dropdown_BarY2_plot,dropdown_BarX_plot):
    figure = go.Figure(data=[
            go.Bar(name = dropdown_BarY1_plot,x=df[dropdown_BarX_plot].unique(), y = list(df[df[dropdown_BarX_plot] == i][dropdown_BarY1_plot].mean() for i in df[dropdown_BarX_plot].unique())),
            go.Bar(name = dropdown_BarY2_plot,x=df[dropdown_BarX_plot].unique(), y = list(df[df[dropdown_BarX_plot] == i][dropdown_BarY2_plot].mean() for i in df[dropdown_BarX_plot].unique()))
        ])
    return figure

@app.callback(
    dash.dependencies.Output('Pie Plot Graph','figure'),
    [dash.dependencies.Input('dropdown Pie plot','value')]
)

def update_Pie_plot(dropdown_Pie_plot):
    figure = px.pie(df,
                    values = dropdown_Pie_plot,
                    names='Claim Type'
                    )
    return figure

if __name__ == '__main__':
    app.run_server(port=5000,debug=True)