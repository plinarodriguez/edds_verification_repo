import os
import numpy as np
import pandas as pd

# Extracts cross sectional data including x,y,z,r,T,volume
# takes long to process data for finest mesh 
# only computing for a single z position within the case solid

import all_functions

##########################
##### Set the Correct Directories for the VTK files
##########################
vtk_directoryM0 = 'study_m0/VTK'
directoryM0 = 'study_m0'
vtk_directoryM1 = 'study_m1/VTK'
directoryM1 = 'study_m1'
vtk_directoryM2 = 'study_m2/VTK'
directoryM2 = 'study_m2'

#z position 
z = 0.0620625  # middle of the geometry with the shorter inlet pipex1.25 . Note the middle of the case is 0.0675 of the 90mm geometry.
region = 'pipeFluid' #'caseSolid'

###############################################
########### Process data for Mesh 0 ########### 
###############################################
ratio = 0.75    
timesM0 = [0,]
for item in os.listdir(directoryM0):
    full_path = os.path.join(directoryM0,item)
    if os.path.isdir(full_path) and item[0:].replace('.','').isdigit():
        timesM0.append(float(item))
timesM0.sort(key=lambda x: float(x))
timesM0 = timesM0[1:]

# timesteps is a list but I just need one timestep
data_T_M0, data_points_M0, data_centroid_M0,data_volumes_M0 = all_functions.temp_points(vtk_directoryM0,z,timesM0,ratio, region) #
print(f'data_T_M0={data_T_M0}')
z1_0,m1_0 = z*np.ones_like(data_T_M0[-1]),np.zeros_like(data_T_M0[-1])
print('finished processing Mesh 0')
###############################################
########### Process data for Mesh 1 ########### 
###############################################
ratio = 0.75
timesM1 = [0,]
for item in os.listdir(directoryM1):
    full_path = os.path.join(directoryM1,item)
    if os.path.isdir(full_path) and item[0:].replace('.','').isdigit():
        timesM1.append(float(item))
timesM1.sort(key=lambda x: float(x))
timesM1 = timesM1[1:]
data_T_M1, data_points_M1, data_centroid_M1,data_volumes_M1 = all_functions.temp_points(vtk_directoryM1,z,timesM1,ratio,region)
z1_1,m1_1 = z*np.ones_like(data_T_M1[-1]),np.ones_like(data_T_M1[-1])
print('finished processing Mesh 1')
###########################################################
#### Convert data_centroid into x,y points and radii ###### 
###########################################################
data_m0 = pd.DataFrame()
data_m1 = pd.DataFrame()
# data_m2 = pd.DataFrame()
for indx, t in enumerate(timesM0):
    xM0_all, yM0_all, rM0_all = [],[],[] 
    xM1_all, yM1_all, rM1_all = [],[],[]
    data_centroids_M0 = data_centroid_M0[indx] # taking the last timestep data only [-1]
    data_centroids_M1 = data_centroid_M1[indx]
    xM0,yM0 = data_centroids_M0[:,0],data_centroids_M0[:,1]
    xM1,yM1 = data_centroids_M1[:,0],data_centroids_M1[:,1]
    rM0, rM1 = np.sqrt(xM0**2 +yM0**2), np.sqrt(xM1**2 +yM1**2)
    xM0_all.append(xM0)
    yM0_all.append(yM0) 
    xM1_all.append(xM1)
    yM1_all.append(yM1)
    rM0_all.append(rM0)
    rM1_all.append(rM1)
    ##################################################################
    #### Build dataframe for Mesh 0 data (Mesh,z,x,y,r,T,U,Vol) ###### 
    ##################################################################
    df_tmp = pd.DataFrame({'Mesh':m1_0,'z':z1_0,'x':xM0_all[0],'y':yM0_all[0],'r':rM0_all[0],
                                'T':data_T_M0[indx],'Vol':data_volumes_M0[indx]})
    df_tmp['time']= t
    data_m0 = pd.concat([data_m0, df_tmp], ignore_index=True)
    ##################################################################
    #### Build dataframe for Mesh 1 data (Mesh,z,x,y,r,T,U,Vol) ###### 
    ##################################################################
    df1_tmp = pd.DataFrame({'Mesh':m1_1,'z':z1_1,'x':xM1_all[0],'y':yM1_all[0],'r':rM1_all[0],
                                    'T':data_T_M1[indx],'Vol':data_volumes_M1[indx]})
    df1_tmp['time']= t
    data_m1 =  pd.concat([data_m1, df1_tmp], ignore_index=True)
##################################################
###### Combine all mesh dataframes
##################################################
data_mAll = pd.concat([data_m0,data_m1])
##################################################
###### Save to a csv file one directory above
##################################################
data_mAll.to_csv(f'data/dataT_m01_{region}.csv',index=False, float_format='%.15g')
