import numpy as numpy
import matplotlib.pyplot as plt
from gen_pml import *

from ugv import *
# Add other libraries from where planning is reqd.
from UAV_only import *
from Orienteering_UAV_UGV import *


def plot_tour(pml_pts, uav_points, ugv_points):
    pass 

if __name__=="__main__":
    # Define 

    # Grid size
    grid_size = (500,500)
    # Number of PML points
    num_pml = (40)
    # Radius of visibility of UAV C
    C = 100
    resolution = C / math.sqrt(2)
    # Battery Life of UAV
    Battery = 300
    #Takeoff/Landing cost
    Ca = 80
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

    fig, axs = plt.subplots(3)

    #UAV path with UGV
    starting_node1,path_matrix1, visited_PML1,E1,V1 = UAV_UGV(pml_pts,resolution,Ca,Battery,grid_size)
    #Path using only UAV
    starting_node2,path_matrix2, visited_PML2,E2,V2=UAV_only(pml_pts, resolution, Ca, Battery, grid_size)

    for x in range(math.ceil(grid_size[0] / resolution)):
        axs[0].axvline(x * resolution, color='black', linestyle='--')
    for y in range(math.ceil(grid_size[1] / resolution)):
        axs[0].axhline(y * resolution, color='black', linestyle='--')
    axs[0].scatter(pml_pts[:, 0], pml_pts[:, 1], s=40, color='gray', marker='*')
    axs[0].scatter([E1[V1, 0]], [E1[V1, 1]], s=20, color='r', marker='s')
    for v in V1:
        axs[0].annotate(int(E1[v, 2]), (E1[v, 0], E1[v, 1]), textcoords="offset points", xytext=(0, 10), ha='center',
                        color='red', size=20)

    axs[1].scatter(pml_pts[:, 0], pml_pts[:, 1], s=40, color='gray', marker='*')
    for i in range(path_matrix2.shape[0]):
        axs[1].plot([path_matrix2[i, 0], path_matrix2[i, 2]], [path_matrix2[i, 1], path_matrix2[i, 3]], color='r', linestyle='--')
    axs[1].scatter([starting_node2[0]], [starting_node2[1]], s=20, color='b', marker='s')

    axs[2].scatter(pml_pts[:, 0], pml_pts[:, 1], s=40, color='gray', marker='*')
    for i in range(path_matrix1.shape[0]):
        if path_matrix1[i, 4] == 0:
            axs[2].plot([path_matrix1[i, 0], path_matrix1[i, 2]], [path_matrix1[i, 1], path_matrix1[i, 3]], color='r',
                        linestyle='--')
        else:
            axs[2].scatter([path_matrix1[i, 0], path_matrix1[i, 2]], [path_matrix1[i, 1], path_matrix1[i, 3]], s=20,
                           color='r', marker='s')
    axs[2].scatter([starting_node1[0]], [starting_node1[1]], s=20, color='b', marker='s')

    plt.show()


    # Feed in Subset of PML points to UGV Planning. 
    # RETURN UGV tour in ordered list (x, y)
    ugv_points = ugv_planning(pml_pts_subset, algo= "On2" )  # algo On2(O(rmax2/rmin2))  On1(O(rmax/rmin))


    # Plot PML points, UAV tour, UGV tour. 
    # plot_tour(pml_pts, uav_points, ugv_points)
