from __future__ import division, print_function
import numpy as np
import cv2
import random
import pandas as pd

import math, copy

# from tspy import TSP
# from tspy.solvers import NN_solver
# from tspy.solvers import TwoOpt_solver

from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
# import shapely.geometry as sgeom

# import cartopy.crs as ccrs
# import cartopy.io.shapereader as shpreader

def rand_num(min, max):
    return random.randint(min, max)

def pml(number):

    pml_points = []

    for num in range(number):

        radius = rand_num(rad_min, rad_max)

        x = rand_num(x_min, x_max)
        y = rand_num(y_min, y_max)


        pml_points.append([x,y,radius])

    pml_points = np.array(pml_points)

    return pml_points

def draw(points):
    
    canvas = np.ones((x_max, y_max))

    for point in points:
        x = point[0]
        y = point[1]
        radius = point[2]

        cv2.circle(canvas, (x,y), radius, (0,0,0), 2)
    
    cv2.imshow('PML', canvas) 
    cv2.waitKey()  


def transform(pair, xmin, xmax, ymin, ymax):
    x = pair[0]
    y = pair[1]
    return [(x-xmin)*100/(xmax - xmin), (y-ymin)*100/(ymax - ymin)]

def tspn_plot(points):

    points = points.values
    
    canvas = np.ones((x_max, y_max))

    points = np.vstack((points, [points[0]]))

    i = 0
    x_arr = []
    y_arr = []

    for point in points:    

        x = point[0]
        y = point[1]

        x_arr.append(x)
        y_arr.append(y)

        i = i+1

        cv2.circle(canvas, (x,y), 2, (0,0,0), 2)
        
    for i in range(len(x_arr)-1):
        cv2.line(canvas, (x_arr[i],y_arr[i]), (x_arr[i+1],y_arr[i+1]), (0,0,0), 2)

    cv2.imshow('TSPN', canvas) 
    cv2.waitKey()  

def tspn(points):

# OLD METHOD
    # tsp = TSP()

    # tsp.read_data(points)

    # sol = NN_solver()
    # tsp.get_approx_solution(sol)

    # tsp.plot_solution('NN_solver')

    # sol = TwoOpt_solver(list(a.tours.values())[0],500)
    # tsp.get_approx_solution(sol)
    # tsp.plot_solution('TwoOpt_solver')

    # best_tour = tsp.get_best_solution()
    points = points[0:,0:2]

    points_pd = pd.DataFrame({'x': points[:, 0], 'y': points[:, 1]})

    # Instantiate solver
    solver = TSPSolver.from_data(
        points[0:, 0],
        points[0:, 1],
        norm="GEO"
    )

    # Find tour
    tour_data = solver.solve()
    assert tour_data.success

    solution = points_pd.iloc[tour_data.tour]
    print("Optimal tour:")
    print(u' -> '.join(
        '{r.x}, {r.y}'.format(r=row) for _, row in solution.iterrows()))

## PLOTTING

    # ax = plt.axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
    # ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    # shapename = 'tour'
    # states_shp = shpreader.natural_earth(resolution='110m',
    #                                      category='cultural', name=shapename)

    # ax.background_patch.set_visible(False)
    # ax.outline_patch.set_visible(False)

    # tour = sgeom.LineString(list(zip(solution.x, solution.y)))
    # capitals = sgeom.MultiPoint(list(zip(solution.x, solution.y)))

    # for state in shpreader.Reader(states_shp).geometries():
    #     facecolor = [0.9375, 0.9375, 0.859375]
    #     edgecolor = 'black'

    #     ax.add_geometries([state], ccrs.PlateCarree(),
    #                       facecolor=facecolor, edgecolor=edgecolor)

    # ax.add_geometries([tour], ccrs.PlateCarree(),
    #                   facecolor='none', edgecolor='red')
    # for x, y in zip(solution.x, solution.y):
    #     ax.plot(y, x, 'ro', transform=ccrs.PlateCarree())
        
    # plt.savefig("optimal_tour.png", bbox_inches='tight')
    # plt.show()

    tspn_plot(solution)

def check_circle(circ1, circ2):

    x1 = circ1[0]
    y1 = circ1[1]
    r1 = circ1[2]

    x2 = circ2[0]
    y2 = circ2[1]
    r2 = circ2[2]
    
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);  
    radSumSq = (r1 + r2) * (r1 + r2);  
    if (distSq == radSumSq): 
        return 1 
    elif (distSq > radSumSq): 
        return -1 
    else: 
        return 0 


def MIS(pml_point_set):

    I = []

    i = 0

    ref_set = pml_point_set.copy()

    while(pml_point_set.size!=0):

        # np.delete(pml_point_set,i)
        print("Checking with {}".format(pml_point_set[i]))

        i = i+1

        for j in range(0,len(ref_set)):

            print(len(ref_set))

            cond = (pml_point_set[j-1] != pml_point_set[i-1]).all()

            val = check_circle(pml_point_set[i-1], pml_point_set[j-1])
            
            if (cond==True):
                if (val==0) or (val == 1):
                    print("Deleting {}".format(pml_point_set[j-1]))
                    np.delete(ref_set,j)
                    print("Length after deleting is {}".format(print(len(ref_set))))

    return np.array(ref_set)


def main():

    points = pml(30)

    # To draw the points
    # draw(points)

    # start_idx = random.randint(0,len(points))
    # starting_point = points[start_idx]
    print(len(points))

    points = MIS(points)

    draw(points)

    tspn(points)


if __name__ == '__main__':
    
    rad_max = 10
    rad_min = 1
    
    x_min = 0
    x_max = 500

    y_min = 0
    y_max = 500

    main()