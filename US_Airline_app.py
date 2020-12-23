import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

### read in three datasets
airlines = pd.read_csv('airlines.csv')
flights = pd.read_csv('flights.csv')
airports = pd.read_csv('airports.csv')

#exclude columns that are not needed, to make it more clean
flights = flights[['AIRLINE','ORIGIN_AIRPORT','DESTINATION_AIRPORT']]
airports = airports.loc[:,['IATA_CODE','AIRPORT','LATITUDE','LONGITUDE','CITY']]

# calculate #flights at each airport of each airline
temp1=flights.groupby(['AIRLINE','DESTINATION_AIRPORT']).count().reset_index()
temp1.columns = ['AIRLINE','DESTINATION_AIRPORT','#flights']

#Inner join the result to airport dataset, to get the longtitude and lantitude
result_destination = temp1.merge(airports,left_on = 'DESTINATION_AIRPORT', right_on = 'IATA_CODE')



app.layout = html.Div([

    html.H1(children='Please select the Airline you are interested in!'),

    html.Div(children = '''
            This application will show you #flights at each airport at your choice of airline!
            '''),
    dcc.Dropdown(
            id='airline',
            options=[{'label': i, 'value': j} for [i,j] in zip(airlines['AIRLINE'].unique(),airlines['IATA_CODE'].unique())],
            value='AA'
            ),
    dcc.Graph(id='graph')

])


@app.callback(
    Output('graph', 'figure'),
    Input('airline', 'value'))
def update_figure(selected_airline):
    filtered_df = result_destination[result_destination['AIRLINE']  == selected_airline]

    fig = px.scatter_geo(filtered_df,
                    lat='LATITUDE',
                    lon='LONGITUDE',
                    hover_name="DESTINATION_AIRPORT",
                    size="#flights",
                    color = "#flights")

    fig.update_layout(
            title = 'Number of flights by Airline in US airports',
            geo = dict(
                scope='usa',
                projection_type='albers usa',
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(123, 123, 422)",
                countrycolor = "rgb(221, 123, 123)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            )
    )

    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)