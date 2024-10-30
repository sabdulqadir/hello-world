import pandas as pd
import plotly.express as px
from datetime import datetime

def create_housing_map(csv_file):
    """
    Creates an interactive choropleth map of housing sales by state
    
    Parameters:
    csv_file (str): Path to the CSV file containing housing data
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Get the most recent date column (last column)
    latest_date = df.columns[-1]
    
    # Group by state and sum the sales for the most recent date
    state_sales = df.groupby('StateName')[latest_date].sum().reset_index()
    
    # Create the choropleth map
    fig = px.choropleth(
        state_sales,
        locations='StateName',
        locationmode='USA-states',
        color=latest_date,
        scope='usa',
        color_continuous_scale='Viridis',
        labels={latest_date: 'Number of Houses Sold'},
        title=f'Housing Sales by State ({latest_date})'
    )
    
    # Update layout
    fig.update_layout(
        geo=dict(
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        width=1000,
        height=600
    )
    
    return fig

def create_time_series_map(csv_file):
    """
    Creates an animated choropleth map showing housing sales over time
    
    Parameters:
    csv_file (str): Path to the CSV file containing housing data
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Get all date columns (excluding the first 5 columns which are metadata)
    date_columns = df.columns[5:]
    
    # Create a long format dataframe for animation
    data_frames = []
    for date in date_columns:
        temp_df = df.groupby('StateName')[date].sum().reset_index()
        temp_df['Date'] = date
        data_frames.append(temp_df)
    
    long_df = pd.concat(data_frames)
    
    # Create the animated choropleth map
    fig = px.choropleth(
        long_df,
        locations='StateName',
        locationmode='USA-states',
        color=date,
        scope='usa',
        animation_frame='Date',
        color_continuous_scale='Viridis',
        labels={date: 'Number of Houses Sold'},
        title='Housing Sales by State Over Time'
    )
    
    # Update layout
    fig.update_layout(
        geo=dict(
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        width=1000,
        height=600
    )
    
    # Update animation settings
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 100
    
    return fig

# Example usage:
if __name__ == "__main__":
    # Replace with your CSV file path
    csv_file = "./metro.csv"
    
    # Create static map for most recent date
    static_map = create_housing_map(csv_file)
    static_map.show()
    
    # Create animated map showing changes over time
    animated_map = create_time_series_map(csv_file)
    animated_map.show()