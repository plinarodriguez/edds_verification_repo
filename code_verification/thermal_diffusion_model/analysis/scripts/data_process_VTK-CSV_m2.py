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
vtk_directoryM2 = 'study_m2/VTK'
directoryM2 = 'study_m2'

#z position 
z = 0.0620625  # middle of the geometry with the shorter inlet pipex1.25 . Note the middle of the case is 0.0675 of the 90mm geometry.
region = 'pipeFluid' #'caseSolid'

###############################################
########### Process data for Mesh 2 ########### 
###############################################
ratio =  0.75
times_M2 = [0,]
for item in os.listdir(directoryM2):
    full_path = os.path.join(directoryM2,item)
    if os.path.isdir(full_path) and item[0:].replace('.','').isdigit():
        times_M2.append(float(item))
times_M2.sort(key=lambda x: float(x))
times_M2 = times_M2[1:]
data_T_M2, data_points_M2, data_centroid_M2,data_volumes_M2 = all_functions.temp_points(vtk_directoryM2,z,times_M2,ratio,region)
df_T_M2 = pd.DataFrame(data_T_M2)
df_points_M2 = pd.DataFrame(data_points_M2)
df_centroid_M2 = pd.DataFrame(data_centroid_M2)
df_volumes_M2 = pd.DataFrame(data_volumes_M2)

df_T_M2.to_csv('data_T_M2.csv',index=False, float_format='%.15g')
print(f'saved data_T_M2')
df_points_M2.to_csv('data_points_M2.csv',index=False, float_format='%.15g')
print(f'saved data_points_M2')
df_centroid_M2.to_csv('data_centroid_M2.csv',index=False, float_format='%.15g')
print(f'saved data_centroid_M2')
df_volumes_M2.to_csv('data_volumes_M2.csv',index=False, float_format='%.15g')
print(f'saved data_volumes_M2')
z1_2,m1_2 = 1*np.ones_like(data_T_M2[-1]),2*np.ones_like(data_T_M2[-1])
print('finished processing Mesh 2')

###########################################################
#### Convert data_centroid into x,y points and radii ###### 
###########################################################
data_m2 = pd.DataFrame()
for indx, t in enumerate(timesM2):
    xM2_all, yM2_all, rM2_all = [],[],[]
    data_centroids_M2 = data_centroid_M2[indx]
    xM2,yM2 = data_centroids_M2[:,0],data_centroids_M2[:,1]
    rM2 = np.sqrt(xM2**2 +yM2**2)
    xM2_all.append(xM2)
    yM2_all.append(yM2)
    rM2_all.append(rM2)
    ##################################################################
    #### Build dataframe for Mesh 2 data (Mesh,z,x,y,r,T,U,Vol) ###### 
    ##################################################################
    df2_tmp = pd.DataFrame({'Mesh':m1_2,'z':z1_2,'x':xM2_all[0],'y':yM2_all[0],'r':rM2_all[0],
                                    'T':data_T_M2[indx],'Vol':data_volumes_M2[indx]})
    df2_tmp['time']= t
    data_m2 = pd.concat([data_m2, df2_tmp], ignore_index=True)
##################################################
###### Combine all mesh dataframes
##################################################
data_mAll = pd.concat([data_m2])
##################################################
###### Save to a csv file one directory above
##################################################
data_mAll.to_csv(f'data/dataT_m2_{region}.csv',index=False, float_format='%.15g')
