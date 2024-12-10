"""
Overlay plot of indentation data on an image.

@author: Colin Fletcher
"""
# Plot an overlay

# Arguments:
#   image - Path to the image used for overlay plot 
#   data - dataframe containing at least the x and y coordinates along with 
#          corresponding values of the feature to be plotted
#   feature - Column name of the feature to be plotted
#   pad - (Optional) Extra space, in pixels, on the bottom of the image to
#         omit indentations from the plot. This is to prevent plotting over
#         something like a scale bar.
#   x_col - Name of the column containing the x coordinates, if it differs
#           from "x_transform"
#   y_col - Name of the column containing the y coordinates, if it differs
#           from "z_transform"
#   contour - matplotlib parameters for a contour plot
#   scatter - matplotlib parameters for a scatter plot (passing False will omit scatter)
#   cbar - matplotlib parameters for a colorbar
#
def plot_overlay(IMAGE_PATH,
                 data, 
                 feature,
                 pad = None,
                 smoothing = None,
                 x_col = 'x_transform',
                 y_col = 'z_transform',
                 contour = {'cmap': 'jet',
                            'levels': 12,
                            'alpha': 0.66},
                 scatter = {'color': 'black',
                            'marker': '^',
                            's': 10},
                 cbar = {'fraction': 0.025,
                         'pad': 0.05}
                 ):
    import numpy as np
    from scipy import ndimage 
    import matplotlib.pyplot as plt
    
    # Get background image (SEM image of indentations)
    image = plt.imread(IMAGE_PATH)
    
    # Get x and y max values for image, incorporating y padding adjustment
    y_max, x_max = image.shape
    if not pad:
        pad = 0
    y_max = y_max - pad
    
    # Calculate aspect ratio (x/y) of image
    aspect = x_max/y_max
    
    ## Prepare data for plotting
    data = data[[x_col, y_col, feature]]
    
    ## Remove points outside the image range
    data = data[(data[x_col] >= 0) & (data['x_transform'] <= x_max)]
    data = data[(data[y_col] >= 0) & (data['z_transform'] <= y_max)]
   
    # Prepare contour data
    def prepare_contour(x, y, z):
        # Create grid/matrix
        X, Y, Z = np.meshgrid(x, y, z)
  
        return (X, Y, Z)
        
    # Create Plot
    fig, ax = plt.subplots(figsize=(12*aspect,12))
    ax.imshow(image, cmap='Greys_r')
    
    # Separate x, y, z data and create meshgrid if needed for plotting
    x = data['x_transform']
    y = data['z_transform']
    z = data[feature]
    X, Y, Z = prepare_contour(x, y, z)

    # Plot points at indentations    
    if scatter:
        ax.scatter(x, y, **scatter, zorder=2)
        
    # Smooth contour if specified
    if smoothing:
        x = ndimage.zoom(x, smoothing)
        y = ndimage.zoom(y, smoothing)
        z = ndimage.zoom(z, smoothing)    
    
    # Plot contour overlay
    contourplot = ax.tricontourf(x,y,z, **contour)
        
    # Configure colorbar
    cb = fig.colorbar(contourplot, **cbar) 
    cb.ax.set_title(feature, pad=30, size=22, loc='center')
    cb.ax.tick_params(labelsize=16) 
    
    # Configure plot
    plt.axis('off')    
    plt.tight_layout()
    plt.show()