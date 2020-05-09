# ENPM661-Final_Project
Informative path planning for a collaborative robot system in precision agriculture applications.
Original Authors : Pratap Tokekar, Joshua Vander Hook, David Mulla and Volkan Isle

### Dependencies
* python3 and packages(numpy, matplotlib)
* concorde TSPSolver package

You need the python wrapper of the concorde TSPN. Download and install from [here](https://github.com/jvkersch/pyconcorde/)

### Running code
There are several parameters that affect our the solution. 
* Grid Size
* Number of PML
* Cost to ascent/ Cost to descent
* Battery cost
* UAV Field of View 
To run the code for a default set of parameters, simply run
```
python3 main.py
```

### Sample Results from Implementation
Sample PML points
![Sample PML points](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/pml_points.jpg)
Sample path of UAV for UAV + UGV
![Sample path of UAV for UAV + UGV](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-1.jpg)
Sample path of UAV for UAV only
![Sample path of UAV for UAV only](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-2.jpg)
Disjoint patches from circles that UGV has to visit
![Disjoint patches from circles that UGV has to visit](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-4.jpg)
Subset of points to be visited by UGV
![Subset of points to be visited by UGV](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-3.jpg)
Hitting set solution of the UGV
![Hitting set solution of the UGV](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-5.jpg)
Final TSPN path of the UGV
![Final TSPN path of the UGV](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/4-6.jpg)
Sample Segmentation in detail
![Sample Segmentation in detail](https://github.com/vdorbala/ENPM661-Final_Project/blob/master/Images/pml_segmented.png)

