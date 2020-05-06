import numpy as np
import math

def UAV_UGV(PML,resolution,Ca,budget,grid_size):

    maxw=grid_size[0]
    maxh=grid_size[1]

    #Number of grid areas in x and y axis
    rw=math.ceil(maxw/resolution)
    rh=math.ceil(maxh/resolution)

    #Reward matrix
    E=np.zeros((rw*rh,3))
    #Define rewards in grid
    i=0
    for x in range(rw):
        X=x*resolution+resolution/2
        for y in range(rh):
            Y=y*resolution+resolution/2
            E[i, 0] = X
            E[i,1]=Y
            i+=1

    for point in range(PML.shape[0]):
        for i in range(E.shape[0]):
            up=E[i,1]+resolution/2
            buttom=E[i,1]-resolution/2
            left=E[i,0]-resolution/2
            right=E[i,0]+resolution/2
            if  PML[point,0]>left and PML[point,0]<right and PML[point,1]>buttom and PML[point,1]<up:
                E[i,2]+=1

    #List of vertices with one or more PML points
    V=[]
    for i in range(E.shape[0]):
        if E[i,2]>0:
            V.append(i)

    #Cost map
    W=np.zeros((len(E),len(E),2))
    for i in range(len(V)):
        u=V[i]
        upos=np.array([E[u,0],E[u,1]])
        for j in range(len(V)):
            v=V[j]
            vpos=np.array([E[v,0],E[v,1]])
            Eucdis=round(np.linalg.norm(upos - vpos))
            if Eucdis<Ca:
                flag=0
            else:
                flag=1
            W[V[i],V[j],0]=min(Eucdis,Ca)
            W[V[i],V[j],1]=flag

    #Initialize queue for the Orienteering possible paths
    queue=[]
    #Initialize list to store closed possible final paths
    complete_path=[]
    i=0
    for start in V:
        new_path=np.array([E[start,2],0,start])
        queue.append(new_path)
        print(len(V),i)

        while queue:
            u=queue.pop()
            for v in V:
                if v in u[3:]:
                    continue
                else:
                    cost=u[1]+W[int(u[-1]),int(v),0]
                    if cost>budget:
                        continue
                    else:
                        temp=np.append(u,v)
                        temp[1]=cost
                        if v==u[2]:
                            if len(u)>3:
                                #It has to be considered that when the drone starts the path flying and ends it also flying
                                #there is a takeoff/landing cost that is not considered and should be taken into account
                                if W[int(u[2]),int(u[3]),1]==0 and W[int(u[-1]),v,1]==0:
                                    cost = u[1] + W[int(u[-1]), v, 0] + Ca
                                    if cost>budget:
                                        continue
                                    else:
                                        temp[1]=cost
                                        complete_path.append(temp)
                                else:
                                    complete_path.append(temp)
                            else:
                                complete_path.append(temp)
                        else:
                            reward = u[0] + E[v, 2]
                            temp[0] = reward
                            queue.append(temp)
        i+=1

    #Compute the final path with the best reward
    final_reward=0
    for path in complete_path:
        if final_reward<path[0]:
            final_path=path
            final_reward=path[0]

    starting_node=np.array([E[int(final_path[2]),0],E[int(final_path[2]),1]])

    path_matrix=np.zeros((len(final_path)-3,5))

    for i in range(0,len(final_path)-3):
        path_matrix[i,0]=E[int(final_path[i+2]),0]
        path_matrix[i, 1] = E[int(final_path[i+2]), 1]
        path_matrix[i, 2] = E[int(final_path[i+3]), 0]
        path_matrix[i, 3] = E[int(final_path[i+3]), 1]
        path_matrix[i,4]=W[int(final_path[i+2]),int(final_path[i+3]),1]

    visited_PML=[]
    for point in range(PML.shape[0]):
        for i in range(0,len(final_path)-3):
            up=E[int(final_path[i+2]),1]+resolution/2
            buttom=E[int(final_path[i+2]),1]-resolution/2
            left=E[int(final_path[i+2]),0]-resolution/2
            right=E[int(final_path[i+2]),0]+resolution/2
            if  PML[point,0]>left and PML[point,0]<right and PML[point,1]>buttom and PML[point,1]<up:
                visited_PML.append(PML[point])

    visited_PML=np.array(visited_PML)

    print("Final reward with UAV+UGV:", final_reward)

    return starting_node,path_matrix, visited_PML,E,V
