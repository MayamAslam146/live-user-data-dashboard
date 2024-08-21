import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('users_data.csv')

app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Live User Data Dashboard", style={'fontSize': 40, 'textAlign': 'center'}),  # Increase font size and center

    # Add a dropdown to filter by last name (example of interactivity)
    html.Label("Filter by Last Name:", style={'fontSize': 20}),
    dcc.Dropdown(
        id='name-filter',
        options=[{'label': name, 'value': name} for name in df['Last Name'].unique()],
        multi=True,
        placeholder="Select last names...",
        style={'fontSize': 18, 'width': '50%'}
    ),

    # Display key metrics
    html.Div(id='live-metrics', style={'fontSize': 24, 'marginTop': 20}),  # Increase font size of metrics

    # Graph to display data
    dcc.Graph(id='live-graph'),

    # Interval component
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
], style={'padding': 20})

# Callback to update graph and metrics based on the interval and dropdown input
@app.callback(
    [Output('live-graph', 'figure'),
     Output('live-metrics', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('name-filter', 'value')]
)
def update_graph_live(n, selected_names):
    # Filter data based on selected last names
    filtered_df = df[df['Last Name'].isin(selected_names)] if selected_names else df

    # Create a scatter plot
    fig = px.scatter(filtered_df, x='ID', y='First Name',  # Adjust columns as per your CSV structure
                     size='ID', color='Last Name', hover_name='Email',
                     title='User Data Scatter Plot')

    # Display current metrics
    metrics_display = html.Div([
        html.H3(f"Total Users: {len(filtered_df)}", style={'fontSize': 28}),
        html.H3(f"First User: {filtered_df['First Name'].iloc[0]} {filtered_df['Last Name'].iloc[0]}", style={'fontSize': 24}),
        html.H3(f"Last User: {filtered_df['First Name'].iloc[-1]} {filtered_df['Last Name'].iloc[-1]}", style={'fontSize': 24})
    ])

    return fig, metrics_display

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
