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
        self.intr_pts = np.array(self.interior_pts())

    def __eq__(self, c2):
        result = True
        result = (self.center == c2.center and self.radius == c2.radius)
        return result

    def __hash__(self):
        return hash(repr(self))    
    
    def interior_pts(self):
        idx = np.where( (self.gridy-self.center[0])**2 + (self.gridx-self.center[1])**2 < self.radius**2)
        pts = np.hstack((self.gridy[idx].reshape(-1,1), self.gridx[idx].reshape(-1,1)))
        return pts    

    def interior(self, pt):
        if np.linalg.norm(pt - self.center) <= self.radius:
            return 1
        else:
            return 0


class Patch:
    def __init__(self, pts):
        self.pts = np.array(pts)

    def __and__(self, p):
        if p == None:
            return None      
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
        if self.pts[idx].size == 0:
            return None
        return Patch(self.pts[idx])

def plot_patch(patch_set):
    fig = plt.figure(figsize=(5,5))
    ax = fig.gca()
    ax.set_title('PML Patches')    
    for x in patch_set:
        points = plt.scatter(x.pts[:,0], x.pts[:,1])
        ax.add_artist(points)            
    plt.xlim((0,500))
    plt.ylim((0,500))
    plt.show()    

def hitting_set_patches(circles_list):
    # Ouput a list of patches which are disjoint and whose union is the entire area defined by the circles. 
    patch_set = [Patch(x.intr_pts) for x in circles_list] # Create patch list from Circle list. 
    counter = len(patch_set)                        
    while(1):
        curr_patch = patch_set.pop(0)       
        p_intr = [curr_patch & x for x in patch_set]
        idx = np.where(np.array(p_intr) != None)
        if len(idx[0]) == 0:
            counter -= 1
            patch_set.append(curr_patch)
            if counter == 0:
                break
            else:
                continue
        for i in range(len(p_intr)):
            if p_intr[i] !=None:
                patch_set[i] = patch_set[i] - p_intr[i]
                curr_patch = curr_patch - p_intr[i]
                patch_set.append(p_intr[i])
        patch_set.append(curr_patch)
        counter = len(patch_set)


    plot_patch(patch_set)
    # np.savez("patches", patch_set)
    return patch_set 




def ugv_planning(pml_pts, algo="hitting_set"):

    ####################################### PART 1 ###########################################    
    if algo == "MIS":
    # Find "Xbar" list - Equate all radius of pml pts to max radius of pml pts
    # rmax = np.max(pml_pts[:,2])
    # rmin = np.max(pml_pts[:,2])
        pass
    # pml_pts_rmax = np.hstack((pml_pts[:,0:2], np.array([ pml_pts.shape[0]*[rmax] ]).reshape(-1,1))

            

    # Find the Maximal non-intersecting group "I" (MIS)


    # Costruct a grid for each point in "I" with size 6r x 6r and resolution rmin/sqrt(2)

    # Find TSPN for all such points
####################################### PART 2 ###########################################    
    elif algo=="hitting_set":
        X = np.array([Circle(x) for x in pml_pts]) # Define a array of circles where each circle corresponds to each point
        np.random.seed(0)
        
        # Find unique regions and assigns one point to each
        patch_set = hitting_set_patches(X) # find disjoint patches

        hitting_set_pts = np.array([x.pts[np.random.choice(len(x.pts)-1)] for x in patch_set]) # assign a point to each patch. 

        # Create the set of circles for each point where the point lies in those circles 
        hitting_set_circles = [] # list of all sets of circles

        for i in range(len(hitting_set_pts)): 
            hitting_set_circles.append(set([c for c in X if c.interior(hitting_set_pts[i])]))

        hitting_set_list = hitting_set_circles.copy()    

        # Remove all sets which are subsets of some other sets in the hitting_set_circles list. Essentially would only keep those sets whose union is the entire list of PML circles
        counter = len(hitting_set_circles)
        while(1):
            is_subset = False
            curr_set = hitting_set_circles.pop(0)
            for i in range(len(hitting_set_circles)):
                if curr_set.issubset(hitting_set_circles[i]):
                    is_subset = True
                    counter = len(hitting_set_circles)
            if is_subset == False:
                hitting_set_circles.append(curr_set)
                counter -= 1
                if counter == 0:
                    break

        path_pts = []
        for i in range(len(hitting_set_circles)):
            idx = [j for j,x in enumerate(hitting_set_list) if (hitting_set_circles[i] == x)]
            path_pts.append(hitting_set_pts[idx])
        path_pts = np.array([np.squeeze(x).T for x in path_pts])
        return path_pts
        
    else: 
        return -1


if __name__=="__main__":
    pml_pts = generate_pml((30),(500,500), plot = False)
    # pml_pts = np.array([[30,30,10],[40,30,10],[35,25,10], [60,60,10],[70,60,10],[65,55,10] ])
    # pml_pts = np.array([[30,30,10],[40,30,10],[35,25,10] ])
    plot_pml(pml_pts, radius=True)
    path_pts = ugv_planning(pml_pts, algo="hitting_set")
