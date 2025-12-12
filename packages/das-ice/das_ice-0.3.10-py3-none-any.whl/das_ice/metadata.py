import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to process and apply optic length and GPS data on data

def optic_length(da,metadata_optic,dist='distance'):
    '''
    Compute optic length from metadata
    '''

    meta_op=pd.read_csv(metadata_optic)
    meta_op['optic_distance']=np.cumsum((meta_op.Cable_Start-meta_op.Cable_End).abs()*(1+meta_op.Loop))

    # Create 'name' DataArray initialized with '-'
    da_res = xr.DataArray([None] * len(da[dist]), dims=[dist])

    i_start = 0
    i=0
    for i_end in meta_op.optic_distance:
        # Create a boolean mask for the range between i_start and i_end
        npa = ((da[dist] > i_start) & (da[dist] < i_end)).values
        
        # Check if there are any True values in the mask
        if np.any(npa):
            # Ensure you assign a single value (string) to all True positions
            da_res[np.where(npa==True)] = str(meta_op.Name[i] + '-' + meta_op.Type[i])  # Assigning the same single string to all True positions
        
        # Update i_start to the current i_end for the next iteration
        i_start = i_end
        i+=1

    return da_res

def optic_length_plot(da):
    '''
    Plot optic length data
    '''

    # Assuming your DataArray is named optic_length_distance
    # For example:
    optic_length_distance = da

    # Convert xarray DataArray to pandas DataFrame
    df = optic_length_distance.to_dataframe(name='name').reset_index()

    # Drop rows where 'name' is None
    df = df.dropna(subset=['name'])

    # Group by name and calculate the min and max distances
    grouped = df.groupby('name')['distance'].agg(['min', 'max']).reset_index()

    # Generate a unique color for each name using the new method
    colors = plt.get_cmap('tab20', len(grouped))  # You can use other colormaps as well

    # Plot the horizontal bars on a fixed y-coordinate
    plt.figure(figsize=(12, 3))

    # Initialize the y-coordinate for bars
    base_y_position = 0

    # List to store transition points for xticks and their colors
    xticks = []
    xtick_colors = {}

    # Plot bars with different colors
    for idx, row in grouped.iterrows():
        # Plot a horizontal bar
        bar_length = row['max'] - row['min']
        bar_color = colors(idx)
        plt.barh(base_y_position, bar_length, left=row['min'], 
                color=bar_color, edgecolor='black')
        
        # Calculate the midpoint of the bar
        midpoint = (row['max'] + row['min']) / 2
        
        # Add vertical text in the middle of the bar if the bar length is greater than 50
        if bar_length > 50:
            plt.text(midpoint, base_y_position, row['name'],
                    va='center', ha='center', color='black', fontsize=10, rotation=90)
        
        # Add min and max values to xticks if the bar length is greater than 50
        if bar_length > 50:
            xticks.extend([row['min'], row['max']])
            xtick_colors[row['min']] = bar_color
            xtick_colors[row['max']] = bar_color

    # Remove duplicate xticks and sort them
    xticks = sorted(set(xticks))

    # Plot customization
    plt.yticks([base_y_position], [''])  # Hide y-axis label for the single line
    plt.xlabel('Distance')

    # Set xticks at each transition
    plt.xticks(xticks)

    # Customize tick appearance
    ax = plt.gca()

    # Define the offsets for top and bottom positioning
    bottom_offset = 0
    top_offset = 1.05

    # Apply color to xtick labels
    for i, tick in enumerate(ax.get_xticks()):
        tick_label = ax.get_xticklabels()[i]
        tick_value = tick
        color = xtick_colors.get(tick_value, 'black')  # Default to black if not found
        
        # Set the color of the tick label
        tick_label.set_color(color)
        
        # Position the tick labels
        if (i // 2) % 2 == 0:
            # Even pairs: bottom
            tick_label.set_verticalalignment('top')
            tick_label.set_horizontalalignment('right')
            tick_label.set_y(bottom_offset)
        else:
            # Odd pairs: top
            tick_label.set_verticalalignment('bottom')
            tick_label.set_horizontalalignment('left')
            tick_label.set_y(top_offset)
        
        tick_label.set_rotation(90)

    # Hide the axes (lines and labels), keep only the tick labels
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Remove ticks and tick labels from y-axis
    ax.yaxis.set_ticks([])
    ax.set_ylabel('')

    # Adjust layout to ensure labels fit
    plt.tight_layout()
