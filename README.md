# NNS_algorithm
This repository contains sample test data and implementation code of the Nearest Neighbor Score (NNS) algorithm for the comparison of IMU-acquired human arm movements.

To run the code, launch `python NNS.py` on a terminal, and, once requested, insert the name of the dataset subdirectory of your interest (ABD_30, FLEX_50, ROT_10, UC_NST).

The subdirectories contain csv files with four comma-separated values representing the four components (w,x,y,z) of the quaternion associated to the relative rotation between the two IMUs used to acquire data. 
Each subdirectory contains data from the following movements:
* ABD_30:  30° abduction on robotic arm
* FLEX_50: 50° flexion on robotic arm
* ROT_10: 10° external rotation on robotic arm
* UC_NST: Non-standardized <i>Upper Care</i> movement from a human arm 
