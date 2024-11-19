# -*- coding: utf-8 -*-
"""
Test file

Created on Tue Nov 19 08:48:12 2024
@author: Fletcher
"""

#%%

# Path to working and data directories
wd = 'N:\\Samples\\Nanoindentation\\'
data_dir = wd + 'Nanoindentation Data\\Raw Data\\'

# Add working directory to PATH environment variable
import sys
sys.path.append(wd)

# Test run
import parse
import coordinates
import indentplot
result = parse.brukerTDM('N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Raw Data\\')

test_object = indentplot.TestData(result, 
                                  'N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Processed Data\\E-beam_W.txt')

#%%        
import coordinates
# Example usage
image_path = "N:\\Samples\\Nanoindentation\\e-beam_W_Colin\\rbv_nanoindentation_1_0015.tif"
coord, dims = coordinates.label_indents(image_path)
#print(coord)
#%%
results = test_object.results
#transform = coordinates.transform_grid(coord, results)

import math
import numpy as np

# Function to calculate distance between two points
def point_distance(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

# Retrieve point numbers
n1 = int(coord.index[0])
n2 = int(coord.index[1])

# Calculate pixel distance between the two specified points
pt1_px = tuple(coord.loc[n1])
pt2_px = tuple(coord.loc[n2])
pixel_distance = point_distance(pt1_px, pt2_px)

# Calculate physical distance between the two specified points
pt1 = tuple(results.loc[n1][['Stage X (mm)', 'Stage Z (mm)']])
pt2 = tuple(results.loc[n2][['Stage X (mm)', 'Stage Z (mm)']])
phys_distance = point_distance(pt1, pt2)



## Rotate grid so second point coincides with its location on image
# Calculate angle (in radians) of line between pixel points
theta_1 = math.atan((pt1_px[1] - pt2_px[1])/(pt1_px[0] - pt2_px[0]))

# Calculate angle (in radians) of line between transform points
theta_2 = math.atan((pt1[1] - pt2[1])/(pt1[0] - pt2[0]))

# Calculate rotation angle
angle = theta_2 - theta_1

# Perform rotation of set of coordinates
def rotate_grid(x, z, angle):
    # Store grid coordinates in array
    grid = np.array([(x,z) for x,z in zip(x,z)])
    
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    grid_rotated = grid @ rotation_matrix.T
    
    import matplotlib.pyplot as plt
    plt.scatter(grid[:,0], grid[:,1]) # Plot initial position
    plt.scatter(grid_rotated[:,0], grid_rotated[:,1]) # Plot rotated position
    
    # Convert matrix back to lists
    x_coord = grid_rotated[:,0]
    z_coord = grid_rotated[:,1]
    
    return x_coord, z_coord

x_rotated, z_rotated = rotate_grid(results['Stage X (mm)'], results['Stage Z (mm)'], angle)
results['x_transform'] = x_rotated
results['z_transform'] = z_rotated

# Calculate scale factor between pixel and physical distances and scale coordinates
scale = pixel_distance/phys_distance
results['x_transform'] = results['Stage X (mm)'] * scale
results['z_transform'] = results['Stage Z (mm)'] * scale

# Translate grid so first point coincides with its location on image
x_translate = coord.loc[n1]['x_pixels'] - results.loc[n1]['x_transform'] 
z_translate = coord.loc[n1]['y_pixels'] - results.loc[n1]['z_transform'] 
results['x_transform'] = results['x_transform'] + x_translate
results['z_transform'] = results['z_transform'] + z_translate


# Check coordinate transformation
def test_plot():
    import matplotlib.pyplot as plt
    bg_image = plt.imread(image_path)
    fig, ax = plt.subplots(figsize=(12,12))
    ax.imshow(bg_image, cmap='Greys_r')
    plt.scatter(results['x_transform'],
                results['z_transform'])
    
test_plot()









