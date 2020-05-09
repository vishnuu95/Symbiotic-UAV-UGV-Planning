import numpy as numpy
import matplotlib.pyplot as plt
from gen_pml import *

from ugv import *
# Add other libraries from where planning is reqd.
from UAV_only import *
from Orienteering_UAV_UGV import *
from tspn import *

# Add other libraries from where planning is read.

def plot_tour(pml_pts, uav_points, ugv_points):
    pass 

if __name__=="__main__":
    # Define 

    # Grid size
    grid_size = (500,500)
    # Number of PML points
    num_pml = (30)
    # Radius of visibility of UAV C
    C = (80)
    resolution = C / math.sqrt(2)
    # Battery Life of UAV
    Battery = (450)
    #Takeoff/Landing cost
    Ca = (150)
    # .......

    # Generate the PML points
    # RETURN the (x,y,r) 
    pml_pts = generate_pml(num_pml, grid_size, plot = False)

    # Feed In PML points to UAV planning.
    # Feed In Radius of visibility of UAV C.
    # Feed In Takeoff/Landing cost.
    # Feed In Battery Life of UAV.
    # Feed In grid size.
    # RETURN starting vertex.
    # RETURN UAV tour as a list of vertex visited in order.
    # RETURN Subset of PML points in order of grid cells (x, y, r).
    # RETURN UAV tour reward matrix E as (x,y,Reward).
    # RETURN Subset of vertex V with one or more PML points.

    #UAV path with UGV
    starting_node1,path_matrix1, visited_PML1,E1,V1 = UAV_UGV(pml_pts,resolution,Ca,Battery,grid_size)
    #Path using only UAV
    starting_node2,path_matrix2, visited_PML2,E2,V2=UAV_only(pml_pts, resolution, Ca, Battery, grid_size)

    print(np.shape(visited_PML1))
    # Feed in Subset of PML points to UGV Planning. 
    # RETURN UGV tour in ordered list (x, y)
    ugv_points = ugv_planning(np.array(visited_PML1), algo= "hitting_set" )  # algo On2(O(rmax2/rmin2))  On1(O(rmax/rmin))

    tspn(ugv_points)


    # Plot PML points, UAV tour, UGV tour. 
    # plot_tour(pml_pts, uav_points, ugv_points)
