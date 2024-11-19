# -*- coding: utf-8 -*-
"""
Test file

To install from github:
    
    pip install git+https://github.com/LongleafMaterials/indentplot.git --trusted-host github.com

Created on Tue Nov 19 08:48:12 2024
@author: Fletcher
"""

# Path to working and data directories
wd = 'N:\\Samples\\Nanoindentation\\'
data_dir = wd + 'Nanoindentation Data\\Raw Data\\'

# Add working directory to PATH environment variable
import sys
sys.path.append(wd)
#%%
# Test run
USE_PACKAGE = True

if USE_PACKAGE == True:
    import indentplot as ind
    #from indentplot import parse
'''
else:
    import parse
    import coordinates
    import indentplot
'''

import pandas as pd

TEST_RESULT_FILE = 'N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Processed Data\\E-beam_W.txt'
DATA_FOLDER = 'N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Raw Data\\'

# Parse/process Bruker data files
parsed_data = ind.parse_brukerTDM(DATA_FOLDER)
test_data = ind.TestData(parsed_data, TEST_RESULT_FILE)

### Example usage
# Path to image for overlay
image_path = "N:\\Samples\\Nanoindentation\\e-beam_W_Colin\\rbv_nanoindentation_1_0015.tif"
#%%
# Prompt user to pick two points and provide the point numbers as defined by the test - this is used to fit the grid
coord = ind.label_indents(image_path)

# Fit physical coordinates (typ. mm) to image pixel coordinates
# Function returns a dataframe where:
#  - Index is the indent number
#  - x_transform & z_transform are the pixel coordinates
pixel_coord = ind.grid_transform(coord, 
                                 test_data.results)

# Add pixel coordinates to the test results
results = pd.merge(test_data.results, 
                   pixel_coord, 
                   left_index=True, 
                   right_index=True)

#%%
# Function to plot point coordinates overlaid on image to check fit
import matplotlib.pyplot as plt
def test_plot(x,z):
    bg_image = plt.imread(image_path)
    fig, ax = plt.subplots(figsize=(12,12))
    ax.imshow(bg_image, cmap='Greys_r')
    plt.scatter(x, z,
                marker='+',
                s=120,
                lw=0.6,
                #facecolors='none',
                c='black',
                alpha=1,
                #edgecolor='black'
                )
    
# Plot pixel coordinates on the specified image to check fit
test_plot(results.x_transform,
          results.z_transform)

