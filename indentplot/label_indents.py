# -*- coding: utf-8 -*-
"""
User selection of reference indentations (part of coordinate transformation)

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
        
        # After the third entry, reset counter and close window
        if counter > len(position):
            counter = 1
            cv2.destroyAllWindows()
            
        # Prompt for user input
        if event == cv2.EVENT_LBUTTONDOWN:
            indent_number = prompt(f'Indentation number for {position[counter]}:')
            indent_number = int(indent_number)
            
            # Add indentation and coordinates to dataframe
            coord.loc[indent_number] = [x, y]
            
            # Output to console
            print(f'Indent {position[counter]} at ({x}, {y})')

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

