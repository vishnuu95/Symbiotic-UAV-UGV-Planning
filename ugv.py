import numpy as np 
import cv2
import matplotlib.pyplot as plt
# from tspn import *
from gen_pml import *

class Circle:
    gridx, gridy = np.meshgrid(np.arange(0,500),np.arange(0,500))
    def __init__(self, pt):
        self.center = np.array(pt[0:2])
        self.radius = np.array(pt[2])
        self.intr_pts = np.array(self.interior_pts()).reshape(-1,2)
        # print("interior pts", self.intr_pts)

    def __eq__(self, c2):
        result = True
        result = (self.center == c2.center and self.radius == c2.radius)
        return
    
    def interior_pts(self):
        idx = np.where( (self.gridy-self.center[0])**2 + (self.gridx-self.center[1])**2 < self.radius**2)
        return idx    

    def interior(self, pt):
        if np.linalg.norm(pt - self.center) <= self.radius:
            return 1
        else:
            return 0


class Patch:
    def __init__(self, pts):
        self.pts = np.array(pts)

    def __and__(self, p):        
        t = (self.pts[:,None]== p.pts)
        t = t.all(-1)
        idx = np.where(t.any(0), True, False)
        if p.pts[idx].size == 0:
            return None
        return Patch(p.pts[idx])       

    def __sub__(self,p):
        if p == None:
            return self.pts
        t = (p.pts[:,None]==self.pts).all(-1)
        idx = np.where(t.any(0), False, True)
        return Patch(self.pts[idx])


def hitting_set(circles_list):
    
    patch_set = np.array([Patch(x.intr_pts) for x in circles_list])
    patch_added = True
    while(patch_added):
        patch_added = False
        curr_patch = patch_set[0]
        np.delete(patch_set,0)
        p_intr = np.array([curr_patch & x for x in patch_set])
        idx = np.where(p_intr != None)
        if len(idx) != 0:
            patch_added = True
        print("patch set", type(patch_set))
        print("patch intr", type(p_intr))
        patch_set = patch_set - p_intr
        for i in range(len(p_intr)):
            curr_patch -= p_intr[i]
            if p_intr[i] != None:
                np.append(patch_set, p_intr[i])
        patch_set.append(curr_patch)
    print("done!")
    print("patch_set", patch_set)
    return patch_set    


def ugv_planning(pml_pts, algo=True):

    ####################################### PART 1 ###########################################    
    # if algo == "On2":
    # Find "Xbar" list - Equate all radius of pml pts to max radius of pml pts
    # rmax = np.max(pml_pts[:,2])
    # rmin = np.max(pml_pts[:,2])

    # pml_pts_rmax = np.hstack((pml_pts[:,0:2], np.array([ pml_pts.shape[0]*[rmax] ]).reshape(-1,1))

            

    # Find the Maximal non-intersecting group "I" (MIS)


    # Costruct a grid for each point in "I" with size 6r x 6r and resolution rmin/sqrt(2)

    # Find TSPN for all such points
####################################### PART 2 ###########################################    
    if algo==True:
        X = np.array([Circle(x) for x in pml_pts])
        # print(X.shape)
        # input()
        # Find unique regions and assigns one point to each
        patch_set = hitting_set(X)
        
        hitting_set_pts = np.array([np.random.choice(np.array(x.pts)) for x in patch_set])

        # Find set of circles for each point 
        hitting_set_circles = []
        for i in range(hitting_set_pts):
            hitting_set_circles[i] = set([c for c in X if c.interior(hitting_set_pts[i])])

        print(hitting_set_circles)
        input()
        # Find the smallest set of p whose union is the original circle
        merged = True
        while(merged):
            merged = False
            is_subset = False
            curr_set = hitting_set_circles.pop(0)
            for i in range(len(hitting_set_circles)):
                if curr_set[0].issubset(hitting_set_circles[i][0]):
                    merged = True
                    is_subset = True
            if is_subset == False:
                hitting_set_circles.append(curr_set)

        path_pts = [hitting_set_pts[x[1]] for x in hitting_set_circles]

        return path_pts

    else: 
        return -1


if __name__=="__main__":
    pml_pts = generate_pml((30),(500,500), plot = False)
    path_pts = ugv_planning(pml_pts, algo=True)
