from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import pathlib


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv(DATA_PATH.joinpath("babyNamesUSYOB-full.csv"))
# data source: https://www.kaggle.com/datasets/thedevastator/us-baby-names-by-year-of-birth 


app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.Div(
            className='banner row',
            children=[
                html.H2(className='h2-title', children="Baby Names Dashboard")
            ]
        ),
        html.Div(
            className='row app-body',
            children=[
                html.Div(
                    className='four columns',
                    children=[
                        html.Div(
                            className='bg-white',
                            children=[
                                html.Div(
                                    className='padding-top-bot',
                                    children=[
                                        html.H6('Name'),
                                        dcc.Dropdown(df.Name.unique(), id='dropdown-name'),
                                        html.Br(),
                                        html.H6('Sex'),
                                        dcc.RadioItems(['Male', 'Female', 'Combined'], value='Combined', inline=True, id='sex'),
                                        html.Br(),
                                        html.H6('Bin Number'),
                                        dcc.Slider(20, 100, 10, value=50, id='bin-slider')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='eight columns',
                    children=[
                        html.Div(
                            className='bg-white',
                            children=[
                            dcc.Graph(id='main-graph')
                            ]
                        )
                    ]
                )
            ]
        )
        
    ]
)

@callback(
    Output('main-graph', 'figure'),
    Input('dropdown-name', 'value'),
    Input('bin-slider', 'value'),
    Input('sex', 'value')
)
def update_graph(name, bin, sex):
    dff = df[df.Name == name]
    if sex == 'Male':
        dfff = dff[dff.Sex == 'M']
        return px.histogram(dfff, x='YearOfBirth', y='Number', nbins=bin)
    elif sex == 'Female':
        dfff = dff[dff.Sex == 'F']
        return px.histogram(dfff, x='YearOfBirth', y='Number', nbins=bin)
    else:
        return px.histogram(dff, x='YearOfBirth', y='Number', color='Sex', color_discrete_map={'M': 'lightskyblue', 'F': 'lightpink'}, nbins=bin)

if __name__ == '__main__':
    app.run_server(debug=True)