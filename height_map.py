import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal


def create_targets(frame_dimension, target_list, weapon):
    
    width = frame_dimension[0]
    height = frame_dimension[0]
    
    # Generate the values for z
    x, y = np.mgrid[0:width:1, 0:height:1]   # Create meshgrid
    z = 0
    pos = np.dstack((x, y)) # Create array of position
    
    for i in range(target_list.shape[0]):
        hole = multivariate_normal([target_list[i, 0], target_list[i, 1]], [[10 * 10**weapon, 0], [0, 10 * 10**weapon]])  # Create Gaussian for hole
        z += - hole.pdf(pos)    # Get values for z
    
    return x, y, z



def create_civilians(frame_dimension, civilian_list):
    
    width = frame_dimension[0]
    height = frame_dimension[0]
    
    # Generate the values for z
    x, y = np.mgrid[0:width:1, 0:height:1]   # Create meshgrid
    z = 0
    pos = np.dstack((x, y)) # Create array of position
    
    for i in range(target_list.shape[0]):
        bump = multivariate_normal([civilian_list[i, 0], civilian_list[i, 1]], [[100, 0], [0, 100]])  # Create Gaussian for hole
        z += bump.pdf(pos)  # Get values for z
    
    return x, y, z


# CODE TO TEST THE FUNCTIONS

frame_dimension = [600, 400]
target_list = np.array([[50, 30], [450, 200], [200, 350]])
civilian_list = np.array([[100, 80], [600, 100], [300, 10]])
weapon = 0

x, y, z_target = create_targets(frame_dimension, target_list, weapon)
x, y, z_civilian = create_civilians(frame_dimension, civilian_list)

z = z_target + z_civilian

# Plot the 2D graph
fig2d = plt.figure()
ax2d = fig2d.add_subplot(111)
ax2d.contourf(x, y, z)

# Plot the 3D graph 
fig3d = plt.figure()
ax3d = fig3d.gca(projection='3d')
ax3d.plot_surface(x, y, z, cmap='viridis', linewidth=0)