# -*- coding: utf-8 -*-
"""
Sample code for indentplot

"""

### Basic importing data

# Import the indentplot package
import indentplot as ind

# Path to the condensed test result file. For Bruker, this will be a .txt file in 
# fixed width format (FWF) looking somewhat like:
# <name of test file.tdm> <hc value> <Er value> <H value>
#
TEST_RESULT_FILE = '<path to file>'

# Path to the data folder containing all of the indentation result files for processing.
# For Bruker, there is one set of files (.hld, .tdm, .tdx) for every indentation.
#
DATA_FOLDER = '<path to directory containing test data>'

# Parse data (in this case Bruker .tdm format) from the data folder. This will read all of
# the .tdm files (XML-formatted) into a list of dictionaries. Each dictionary contains all
# of the test data for an indentation. Format is a pandas dataframe.
#
parsed_data = ind.parse_brukerTDM(DATA_FOLDER)

# Create an object to store the test data and perform some additional processing. Using this
# object is not essential, but may be convenient if handling multiple data sets.
#
#   .xml -> Same as parsed_data above, i.e., the result from ind.parse_brukerTDM(DATA_FOLDER)
#           Stored as a pandas dataframe.
#   .header -> Data extracted from the XML 'header' property, which is a table of test data
#              for all files processed. Stored as a pandas dataframe.
#   .results -> Data from the TEST_RESULT_FILE, stored as a pandas dataframe.
#
test_data = ind.TestData(parsed_data, TEST_RESULT_FILE)


### Converting to image coordinates

# Path to the image to be used for overlay plots
IMAGE_PATH = "N:\\Samples\\Nanoindentation\\e-beam_W_Colin\\rbv_nanoindentation_1_0015.tif"

# label_indents will open the image at IMAGE PATH. There is not yet a prompt, but the user
# will need to pick two indentations as references for conversion of the physical dimensions,
# e.g., mm, to pixel dimensions in the image.
# 
# Click the first indentation and a prompt will appear to input the indentation number as
# defined in the test data. Select as close to the center of the indent as possible because
# the click sets image coordinates. Repeat this for the second point. It is recommended to
# choose points on opposite corners of the grid.
#
coord = ind.label_indents(IMAGE_PATH)

# ind.grid_transform will take the reference coordinates above and transform the physical
# coordinates to pixel coordinates so that data may be accurately plotted over the image.
# It returns a dataframe with index corresponding to indent number along with coordinates.
pixel_coord = ind.grid_transform(coord, 
                                 test_data.results)

# Appends pixel coordinates to the test results dataframe. This is needed to keep all
# data in one location for plotting.
import pandas as pd
results = pd.merge(test_data.results, 
                   pixel_coord, 
                   left_index=True, 
                   right_index=True)

# Optional, but plotting is recommended to check that the transformed coordinates 
# coincide with indentations on the image. 
#
import matplotlib.pyplot as plt
def test_plot(x,z):
    bg_image = plt.imread(IMAGE_PATH)
    fig, ax = plt.subplots(figsize=(12,12))
    ax.imshow(bg_image, cmap='Greys_r')
    plt.scatter(x, z,
                marker='+',
                s=120,
                lw=0.6,
                c='black')
test_plot(results.x_transform,
          results.z_transform)
