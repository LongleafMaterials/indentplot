# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:22:22 2024
@author: Fletcher
"""

# 
# Generate image pixel coordinates for indentations
#
# First step is to take user input for indentation numbers

import cv2
import tkinter as tk
from tkinter import simpledialog
import pandas as pd

# Incremental counter for corners
counter = 1

# Popup prompting for user to input indentation number
def prompt(prompt_text):
    root = tk.Tk()
    root.withdraw()

    # Create a simple dialog to get input
    result = simpledialog.askstring('Input', prompt_text, parent=root)
    return result


# Label corners for a grid
def label_indents(image_path):
    # Create dataframe to store corner information
    coord = pd.DataFrame(columns=['x_pixels', 'y_pixels'])
        
    # Read specified image
    img = cv2.imread(image_path)

    # Handle mouse click
    def mouse_callback(event, x, y, flags, param):
        global counter
        
        # Define position of coordinates
        position = {1: 'Point 1',
                    2: 'Point 2'}
        
        # After the third entry, close window
        if counter > len(position):
            cv2.destroyAllWindows()
            
        # Prompt for user input
        if event == cv2.EVENT_LBUTTONDOWN:
            indent_number = prompt(f'Indentation number for {position[counter]}:')
            indent_number = int(indent_number)
            #print(f'Coordinates of {indent_number}: ({x}, {y})')
            
            # Add indentation and coordinates to dataframe
            coord.loc[indent_number] = [x, y]
            
            counter += 1
            
    # Define name of image window
    window_name = 'Image'

    # Create a window and display the image, set to a reasonable size, and position it in-screen
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1024, 768) 
    cv2.moveWindow(window_name, 40,30)
    cv2.setMouseCallback(window_name, mouse_callback)
    cv2.imshow(window_name, img)

    # Prompt for grid dimensions
    dims = prompt('Enter grid dimensions (# of indents) in form dim1,dim2:')

    # Wait for a key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return coord, dims

# Transform physical locations to coincide with image locations (real position -> pixel position
def transform_grid(coord, results):
    import math
    
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
    
    # Calculate scale factor between pixel and physical distances and scale coordinates
    scale = pixel_distance/phys_distance
    results['x_transform'] = results['Stage X (mm)'] * scale
    results['z_transform'] = results['Stage Z (mm)'] * scale
    
    # Translate coordinates so that first point coincides with location on image (pixel coordinates)
    #x_translate = 


# Interpolate pixel coordinates of all indentations from corner coordinates and number
# For a grid, need three corner points labeled in the image to determine location and numbers of all points
# Test output has Stage X, Y, Z. Pixel coordinates correlating those
def interpolate_points(coord):
    # Calculate y for given x and two points on line
    def point_slope(x, pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        m = (y2 - y1) / (x2 - x1)
        
        y = m * (x - x1) + y1
        return y


