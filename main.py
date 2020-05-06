import numpy as numpy
import matplotlib.pyplot as plt
from gen_pml import *
# Add other libraries from where planning is reqd.

def plot_tour(pml_pts, uav_points, ugv_points):
    pass 

if __name__=="__main__":
    # Define 

    # Grid size
    grid_size = (500,500)

    # Number of PML points
    num_pml = (40)

    # Radius of visibility of UAV C

    # Battery Life of UAV

    # .......

    # Generate the PML points
    # RETURN the (x,y,r) 
    pml_pts = generate_pml(num_pml, grid_size, plot = False)

    # Feed In PML points to UAV planning.
    # RETURN UAV tour in ordered list(x,y).
    # RETURN Subset of PML points in order of grid cells (x, y, r).
    uav_points, pml_pts_subset = uav_planning(pml_pts)


    # Feed in Subset of PML points to UGV Planning. 
    # RETURN UGV tour in ordered list (x, y)
    ugv_points = ugv_planning(pml_pts_subset)


    # Plot PML points, UAV tour, UGV tour. 
    plot_tour(pml_pts, uav_points, ugv_points)
