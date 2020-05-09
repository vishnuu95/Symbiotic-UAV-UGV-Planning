# ENPM661-Final_Project
Informative path planning for a collaborative robot system in precision agriculture applications.
Original Authors : Pratap Tokekar, Joshua Vander Hook, David Mulla and Volkan Isle

### Dependencies
* python3 and packages(numpy, matplotlib)
* concorde TSPSolver package

You need the python wrapper of the concorde TSPN. Download and install from [here]https://github.com/jvkersch/pyconcorde/

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

