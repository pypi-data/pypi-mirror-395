import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly


def all_trace(da):
    '''
    Plot all the trace using plotly. The number of trace should not be to high.
    '''
    # Determine the number of rows (channels) in da
    num_rows = da.shape[1]

    # Create a subplot with shared x-axes and `num_rows` subplots
    fig = make_subplots(rows=num_rows, cols=1, shared_xaxes=True, subplot_titles=[f'Distance {da.distance[i].values} m' for i in range(num_rows)])

    # Loop through each row to create a plot
    for i in range(num_rows):
        fig.add_trace(go.Scatter(
            x=da['time'].values,
            y=da[:, i].values,
            mode='lines',
            name=f'Distance {i} m'
        ), row=i + 1, col=1)

        # Hide the x-axis label except for the last plot
        if i < num_rows - 1:
            fig.update_xaxes(showticklabels=False, row=i + 1, col=1)

    # Update layout with a tight layout and margin adjustments
    fig.update_layout(
        title='Synchronized Strain Rate Plots',
        xaxis_title='Time',
        yaxis_title='Strain Rate',
        height=300 * num_rows,  # Adjust height dynamically based on the number of plots
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins for a tighter layout
    )

    return fig

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def viz_two_time_series(s1, s2):
    '''
    Visualize two time series in separate subplots with linked zooming.

    :param s1: First time series DataArray (e.g., original signal)
    :type s1: xr.DataArray
    :param s2: Second time series DataArray (e.g., STA/LTA ratio)
    :type s2: xr.DataArray
    :return: Plotly figure object with two subplots
    :rtype: plotly.graph_objects.Figure
    '''
    # Extract time series for plotting (assumed to be the same for both)
    time_series1 = s1.time
    time_series2 = s2.time

    # Convert DataArrays to Pandas for easier plotting
    s1_series = s1.to_pandas()
    s2_series = s2.to_pandas()

    # Create subplots with shared x-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=["Signal 1", "Signal 2"])

    # Add the first signal to the top subplot
    fig.add_trace(go.Scatter(
        x=time_series1, 
        y=s1_series, 
        mode='lines', 
        name='Signal 1'
    ), row=1, col=1)

    # Add the second signal to the bottom subplot
    fig.add_trace(go.Scatter(
        x=time_series2, 
        y=s2_series, 
        mode='lines', 
        name='Signal 2',
        line=dict(color='red')
    ), row=2, col=1)

    # Customize layout for better readability and interactivity
    fig.update_layout(
        title='Visualization of Two Time Series',
        xaxis2_title='Time',  # Label for the bottom graph's x-axis
        yaxis1_title='Amplitude',
        yaxis2_title='Amplitude',
        template='plotly_white',  # You can switch to 'plotly_dark' if preferred
        hovermode='x',  # Sync hover information across both plots
        height=600,  # Adjust plot height for clarity
        showlegend=True  # Show legends for both signals
    )

    # Return the figure object for interactive display
    return fig
