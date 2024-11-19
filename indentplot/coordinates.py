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
            
            # Add indentation and coordinates to dataframe
            coord.loc[indent_number] = [x, y]

            # Incremenet input counter            
            counter += 1
            
    # Define name of image window
    window_name = 'Image'

    # Create a window and display the image, set to a reasonable size, and position it in-screen
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1024, 768) 
    cv2.moveWindow(window_name, 40,30)
    cv2.setMouseCallback(window_name, mouse_callback)
    cv2.imshow(window_name, img)

    # Wait for a key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return coord

# Transform physical locations to coincide with image locations (real position -> pixel position
def transform_grid(coord, test_results):
    import math
    import numpy as np
    
    # Perform a copy so the original dataframe is not affected
    results = test_results.copy()
    
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
    
        # Perform rotation of matrix using a rotation matrix    
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        grid_rotated = grid @ rotation_matrix.T
       
        # Convert matrix back to lists
        x_coord = grid_rotated[:,0]
        z_coord = grid_rotated[:,1]
        
        return x_coord, z_coord
    
    # Rotate grid
    x_rotated, z_rotated = rotate_grid(results['Stage X (mm)'], results['Stage Z (mm)'], angle)
    results['x_transform'] = x_rotated
    results['z_transform'] = z_rotated
              
    # Calculate scale factor between pixel and physical distances and scale coordinates
    scale = pixel_distance/phys_distance
    results['x_transform'] = results['x_transform'] * scale
    results['z_transform'] = results['z_transform'] * scale
    
    # Translate grid so first point coincides with its location on image - points are now mapped to the image
    x_translate = coord.loc[n1]['x_pixels'] - results.loc[n1]['x_transform'] 
    z_translate = coord.loc[n1]['y_pixels'] - results.loc[n1]['z_transform'] 
    results['x_transform'] = results['x_transform'] + x_translate
    results['z_transform'] = results['z_transform'] + z_translate
    
    return results[['x_transform', 'z_transform']]
