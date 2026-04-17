# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),

                                # Task1: Add a dropdown list to enable Launch Site Selection
                                html.Div([dcc.Dropdown(id='site-dropdown',
                                                        options=[
                                                                {'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': sites[0], 'value': sites[0]},
                                                                {'label': sites[1], 'value': sites[1]},
                                                                {'label': sites[2], 'value': sites[2]},
                                                                {'label': sites[3], 'value': sites[3]},
                                                                ],
                                                        value="ALL",
                                                        placeholder="place holder here",
                                                        searchable=True
                                                    ),
                                ]),
                                html.Br(),   

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                html.Div([
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min=0,
                                        max=10000,
                                        step=1000,
                                        value=[min_payload,max_payload]
                                    )
                                ]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Function decorator to specify function input and outputadd callback decorator
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

# add computation to callback function and return graph
def get_pie_chart(entered_site):   
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
        names='Launch Site', 
        color='Launch Site',
        labels=sites,
        title='Total Success Launches for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie(filtered_df , 
        names='class', 
        color='class',
        title=f'Success Launches for {entered_site}')
        return fig

    fig = px.pie(
        filtered_df,
        names='class',
        title=title,
        color='class'
    )
    return fig
    
# Function decorator to specify function input and outputadd callback decorator
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
    )

def get_scatter_chart(entered_site, payload_range):   
    low,high = payload_range

    if entered_site == 'ALL':
        filtered_df = spacex_df
        title = f'Payload vs Success for All Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        title = f'Payload vs Success for {entered_site}'

    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= low) &
        (filtered_df['Payload Mass (kg)'] <= high)
    ]

    fig = px.scatter(
                filtered_df,
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category', 
                #names='scatter chart names', 
                title=title
                )
    return fig

# Run the app while debug will cause loading delay
if __name__ == '__main__':
    app.run()
