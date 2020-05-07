import numpy as np 
import cv2
import matplotlib.pyplot as plt
from tspn import *

class Circle:
    def __init__(self, pt):
        self.center = pt[0:2]
        self.radius = pt[2]
        

    def interior(self, pt):
        if np.linalg.norm(pt - self.center) <= self.radius:
            return 1
        else:
            return 0    
        

def ugv_planning(pml_pts, algo="On1"):

    if algo == "On2":
        # Find "Xbar" - Equate all radius of pml pts to max radius of pml pts

        # Find the Maximal non-intersecting group "I"

        # Costruct a grid for each point in "I" with size 6r x 6r and resolution rmin/sqrt(2)

        # Find TSPN for all such points
        return path_pts
    elif algo == "On1":
        # Find unique regions and assigns one point to each
        # Find set of circles for each point 
        # Find the smallest set of p whose union is the original circle
        return path_pts
    else: 
        return -1
