import numpy as np
import math
import matplotlib.pyplot as plt

def plot_UAV_only(grid_size, E, V, pml_pts, path_matrix, starting_node, resolution):
    fig, axs = plt.subplots(2, figsize=(5, 5))

    axs[0].set_title('Reward Grid')

    for x in range(math.ceil(grid_size[0] / resolution)):
        axs[0].axvline(x * resolution, color='black', linestyle='--')
    for y in range(math.ceil(grid_size[1] / resolution)):
        axs[0].axhline(y * resolution, color='black', linestyle='--')
    axs[0].scatter(pml_pts[:, 0], pml_pts[:, 1], s=40, color='gray', marker='*')
    axs[0].scatter([E[V, 0]], [E[V, 1]], s=20, color='r', marker='s')
    for v in V:
        axs[0].annotate(int(E[v, 2]), (E[v, 0], E[v, 1]), textcoords="offset points", xytext=(0, 10), ha='center',
                        color='red', size=20)

    axs[1].scatter(pml_pts[:, 0], pml_pts[:, 1], s=40, color='gray', marker='*')
    for i in range(path_matrix.shape[0]):
        axs[1].plot([path_matrix[i, 0], path_matrix[i, 2]], [path_matrix[i, 1], path_matrix[i, 3]], color='r',
                    linestyle='--')
    axs[1].scatter([starting_node[0]], [starting_node[1]], s=20, color='b', marker='s')

    plt.show()


def UAV_only(PML,resolution,Ca,budget,grid_size):

    maxw=grid_size[0]
    maxh=grid_size[1]

    rw=math.ceil(maxw/resolution)
    rh=math.ceil(maxh/resolution)

    E=np.zeros((rw*rh,3))

    budget=budget-Ca

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

    V=[]
    for i in range(E.shape[0]):
        if E[i,2]>0:
            V.append(i)

    W=np.zeros((len(E),len(E)))

    z=0
    for i in range(len(V)):
        u=V[i]
        upos=np.array([E[u,0],E[u,1]])
        for j in range(len(V)):
            v=V[j]
            vpos=np.array([E[v,0],E[v,1]])

            Eucdis=round(np.linalg.norm(upos - vpos))

            W[V[i], V[j]] = Eucdis

    queue=[]
    complete_path=[]
    i=0
    for start in V:
        new_path=np.array([E[start,2],0,start])

        queue.append(new_path)

        print(len(V),i)

        while queue:
            u=queue.pop()
            # print(queue)
            for v in V:

                if v in u[3:]:
                    continue
                else:
                    cost=u[1]+W[int(u[-1]),int(v)]
                    if cost>budget:
                        continue
                    else:

                        temp=np.append(u,v)

                        temp[1]=cost
                        if v==u[2]:
                            complete_path.append(temp)

                        else:
                            reward = u[0] + E[v, 2]
                            temp[0] = reward
                            queue.append(temp)

        i+=1
    final_reward=0
    for path in complete_path:
        if final_reward<path[0]:
            final_path=path
            final_reward=path[0]

    starting_node=np.array([E[int(final_path[2]),0],E[int(final_path[2]),1]])



    path_matrix=np.zeros((len(final_path)-3,4))

    for i in range(0,len(final_path)-3):
        path_matrix[i,0]=E[int(final_path[i+2]),0]
        path_matrix[i, 1] = E[int(final_path[i+2]), 1]
        path_matrix[i, 2] = E[int(final_path[i+3]), 0]
        path_matrix[i, 3] = E[int(final_path[i+3]), 1]

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

    print("Final reward with UAV only:",final_reward)

    plot_UAV_only(grid_size, E, V, PML, path_matrix, starting_node, resolution)

    return starting_node,path_matrix, visited_PML,E,V
