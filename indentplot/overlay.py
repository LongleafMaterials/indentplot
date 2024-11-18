"""
WIP

Created on Mon Sep 30 09:48:02 2024
@author: Colin Fletcher
"""

import matplotlib.pyplot as plt
import json
import pandas as pd
import sys
import numpy as np
from scipy import ndimage

#
# Plot a map of data overlaid onto an image
#
# Function inputs:
#   data - Object from parse.py containing the data to be plotted
#   coord - Image coordinates, in pixels, for each indentation (format TBD, was JSON for initial tests)
#   image - Path to image file used for overlay

def overlay_map(data, coord, image_file):
    # Get background image (SEM image of indentations)
    bg_image = plt.imread(image_file)
    
    # Image scale (pixels/um)
    # scale = 5.04
    
    # Reference coordinates for indentations visible in image (JSON with same name as image)
    with open(imgPath + image_file.split('.')[0] + '.json') as f:
        ref_coord = json.load(f)
    
    # Extract indentation coordinates
    def coordinates(data, ref_coord):
        coordinates = {}
        for k in data.keys():
            index = int(k[-4:])
            x = data[k]['header']['Stage X'].split(' ')[0]
            y = data[k]['header']['Stage Y'].split(' ')[0]
            coordinates[index] = {'test_x': x,
                                  'test_y': y}
        coordinates = pd.DataFrame.from_dict(coordinates, orient='index')    
        for c in coordinates.columns:
            coordinates[c] = pd.to_numeric(coordinates[c])
        
        # Add columns for image (pixel) coordinates
        coordinates['img_x'] = None
        coordinates['img_y'] = None
    
        # Add pixel coordinates for specified indents
        for k in ref_coord['points'].keys():
            coordinates.loc[int(k),'img_x'] = ref_coord['points'][k]['x']
            coordinates.loc[int(k),'img_y'] = ref_coord['points'][k]['y']
        
        for c in ['img_x', 'img_y']:
            coordinates[c] = pd.to_numeric(coordinates[c])
        
        return coordinates
    
    # Prepare contour data
    def prepare_contour(x, y, z):
        # Get unique values of x and y pixel coordinates
        x_unique = np.sort(x.unique())
        y_unique = np.sort(y.unique())
        
        # Create grid/matrix
        X, Y, Z = np.meshgrid(x, y, z)
    
        return (X, Y, Z)
    
    # Load processed data
    processed_data = pd.read_fwf(dataPath + 'E-beam_W.txt')
    processed_data.columns = ['test file name', 'hc (nm)', 'Er (GPa)', 'H (GPa)']
    processed_data = processed_data.dropna()
    processed_data.reset_index(inplace=True, drop=True)
    
    # Get coordinates of indendations with pixel coordinates and add to data
    processed_data = processed_data.join(coordinates(parsed, ref_coord))
    processed_data = processed_data.dropna()
    
    # Properties to plot and file names for output
    to_plot = {'H (GPa)': image_file.split('.')[0] + '_H.png',
               'hc (nm)': image_file.split('.')[0] + '_hc.png',
               'Er (GPa)': image_file.split('.')[0] + '_Er.png'}
    
    smoothing = False
    for k in to_plot.keys():
        # Property to plot
        prop = k
        
        # Create Plot
        fig, ax = plt.subplots(figsize=(12,12))
        ax.imshow(bg_image, cmap='Greys_r')
        
        # Prepare data for plotting as contour
        x = processed_data['img_x']
        y = processed_data['img_y']
        z = processed_data[prop]
        plot_map = prepare_contour(x, y, z)
    
        # Smooth contour if specified
        if smoothing:
            x = ndimage.zoom(x, 10)
            y = ndimage.zoom(y, 10)
            z = ndimage.zoom(z, 10)    
        
        # Plot contour overlay                             
        contourParams = {'cmap': 'jet',
                         'levels': 12,
                         'alpha': 0.66}
        contourplot = ax.tricontourf(x,y,z, **contourParams)
        
        # Plot points at indentations    
        scatterParams = {'color': 'black',
                         'marker': '^',
                         's': 10}
        ax.scatter(x, y, **scatterParams)
    
    
        # Configure colorbar
        colorbarParams = {'fraction': 0.025,
                          'pad': 0.05}
        cb = fig.colorbar(contourplot, **colorbarParams) 
        cb.ax.set_title(prop, pad=30, size=20, loc='center')
        cb.ax.tick_params(labelsize=16) 
        
        # Configure plot
        plt.axis('off')    
        plt.tight_layout()
        plt.savefig(imgPath + to_plot[k], bbox_inches='tight', dpi=200)
    


