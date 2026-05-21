import os
import numpy as np
import pandas as pd

# import functions and parameters
import params
import all_functions

########################################################################################################################
######     Extracts from VTK files quantities of interest for analysis that are saved to the data directory      #######
########################################################################################################################


##########################
##### Set the Correct Directories for the VTK files
##########################
vtk_directoryM0 = 'study_m0/VTK'
directoryM0 = 'study_m0'
vtk_directoryM1 = 'study_m1/VTK'
directoryM1 = 'study_m1'
vtk_directoryM2 = 'study_m2/VTK'
directoryM2 = 'study_m2'
vtk_directoryM22 = 'study_m2-2/VTK'
directoryM22 = 'study_m2-2'

##########################
##### Begin Processing VTK Data
##########################

###############################################
########### Process data for Mesh 0 ########### 
###############################################
timesM0 = [0,]
ratio = 0.5    
for item in os.listdir(directoryM0):
    full_path = os.path.join(directoryM0,item)
    if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        timesM0.append(float(item))
timesM0.sort(key=lambda x: float(x))
timesM0 = timesM0[1:]
data_T_z1_M0, data_U_z1_M0, data_points_z1_M0, T_bulk_z1_M0, data_centroid_z1_M0,data_volumes_z1_M0 = all_functions.temp_points(vtk_directoryM0,params.z1+0.045,timesM0,ratio) # z=15mm
data_T_z2_M0, data_U_z2_M0, data_points_z2_M0, T_bulk_z2_M0, data_centroid_z2_M0,data_volumes_z2_M0 = all_functions.temp_points(vtk_directoryM0,params.z2+0.045,timesM0,ratio) # z=30mm
data_T_z3_M0, data_U_z3_M0, data_points_z3_M0, T_bulk_z3_M0, data_centroid_z3_M0,data_volumes_z3_M0 = all_functions.temp_points(vtk_directoryM0,params.z3+0.045,timesM0,ratio) # z=45mm
data_T_z4_M0, data_U_z4_M0, data_points_z4_M0, T_bulk_z4_M0, data_centroid_z4_M0,data_volumes_z4_M0 = all_functions.temp_points(vtk_directoryM0,params.z4+0.045,timesM0,ratio) # Hagn Poiseuille Study
ratio_z5 = 0.75
data_T_z5_M0, data_U_z5_M0, data_points_z5_M0, T_bulk_z5_M0, data_centroid_z5_M0,data_volumes_z5_M0 = all_functions.temp_points(vtk_directoryM0,params.z5+0.045,timesM0,ratio_z5)
ratio_z6 = 0.75
data_T_z6_M0, data_U_z6_M0, data_points_z6_M0, T_bulk_z6_M0, data_centroid_z6_M0,data_volumes_z6_M0 = all_functions.temp_points(vtk_directoryM0,params.z6+0.045,timesM0,ratio_z6)
ratio_z7 = 0.75
data_T_z7_M0, data_U_z7_M0, data_points_z7_M0, T_bulk_z7_M0, data_centroid_z7_M0,data_volumes_z7_M0 = all_functions.temp_points(vtk_directoryM0,params.z7+0.045,timesM0,ratio_z7)
z1_0,m1_0 = 1*np.ones_like(data_T_z1_M0[-1]),np.zeros_like(data_T_z1_M0[-1])
z2_0,m2_0 = 2*np.ones_like(data_T_z2_M0[-1]),np.zeros_like(data_T_z2_M0[-1])
z3_0,m3_0 = 3*np.ones_like(data_T_z3_M0[-1]),np.zeros_like(data_T_z3_M0[-1])
z4_0,m4_0 = 4*np.ones_like(data_T_z4_M0[-1]),np.zeros_like(data_T_z4_M0[-1])
z5_0,m5_0 = 5*np.ones_like(data_T_z5_M0[-1]),np.zeros_like(data_T_z5_M0[-1])
z6_0,m6_0 = 6*np.ones_like(data_T_z6_M0[-1]),np.zeros_like(data_T_z6_M0[-1])
z7_0,m7_0 = 7*np.ones_like(data_T_z7_M0[-1]),np.zeros_like(data_T_z7_M0[-1])
print('finished processing Mesh 0')
###############################################
########### Process data for Mesh 1 ########### 
###############################################
ratio = 0.75
timesM1 = [0,]
for item in os.listdir(directoryM1):
    full_path = os.path.join(directoryM1,item)
    if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        timesM1.append(float(item))
timesM1.sort(key=lambda x: float(x))
timesM1 = timesM1[1:]
data_T_z1_M1, data_U_z1_M1, data_points_z1_M1, T_bulk_z1_M1, data_centroid_z1_M1,data_volumes_z1_M1 = all_functions.temp_points(vtk_directoryM1,params.z1+0.045,timesM1,ratio)
data_T_z2_M1, data_U_z2_M1, data_points_z2_M1, T_bulk_z2_M1, data_centroid_z2_M1,data_volumes_z2_M1 = all_functions.temp_points(vtk_directoryM1,params.z2+0.045,timesM1,ratio)
data_T_z3_M1, data_U_z3_M1, data_points_z3_M1, T_bulk_z3_M1, data_centroid_z3_M1,data_volumes_z3_M1 = all_functions.temp_points(vtk_directoryM1,params.z3+0.045,timesM1,ratio)
ratio_z4 = 0.5
data_T_z4_M1, data_U_z4_M1, data_points_z4_M1, T_bulk_z4_M1, data_centroid_z4_M1,data_volumes_z4_M1 = all_functions.temp_points(vtk_directoryM1,params.z4+0.045,timesM1,ratio_z4)
ratio_z5 = 0.5
data_T_z5_M1, data_U_z5_M1, data_points_z5_M1, T_bulk_z5_M1, data_centroid_z5_M1,data_volumes_z5_M1 = all_functions.temp_points(vtk_directoryM1,params.z5+0.045,timesM1,ratio_z5)
ratio_z6 = 0.5
data_T_z6_M1, data_U_z6_M1, data_points_z6_M1, T_bulk_z6_M1, data_centroid_z6_M1,data_volumes_z6_M1 = all_functions.temp_points(vtk_directoryM1,params.z6+0.045,timesM1,ratio_z6)
ratio_z7 = 0.5
data_T_z7_M1, data_U_z7_M1, data_points_z7_M1, T_bulk_z7_M1, data_centroid_z7_M1,data_volumes_z7_M1 = all_functions.temp_points(vtk_directoryM1,params.z7+0.045,timesM1,ratio_z7)
z1_1,m1_1 = 1*np.ones_like(data_T_z1_M1[-1]),np.ones_like(data_T_z1_M1[-1])
z2_1,m2_1 = 2*np.ones_like(data_T_z2_M1[-1]),np.ones_like(data_T_z2_M1[-1])
z3_1,m3_1 = 3*np.ones_like(data_T_z3_M1[-1]),np.ones_like(data_T_z3_M1[-1])
z4_1,m4_1 = 4*np.ones_like(data_T_z4_M1[-1]),np.ones_like(data_T_z4_M1[-1])
z5_1,m5_1 = 5*np.ones_like(data_T_z5_M1[-1]),np.ones_like(data_T_z5_M1[-1])
z6_1,m6_1 = 6*np.ones_like(data_T_z6_M1[-1]),np.ones_like(data_T_z6_M1[-1])
z7_1,m7_1 = 7*np.ones_like(data_T_z7_M1[-1]),np.ones_like(data_T_z7_M1[-1])
print('finished processing Mesh 1')
###############################################
########### Process data for Mesh 2 ########### 
###############################################
ratio =  0.75
times_M2 = [0,]
for item in os.listdir(directoryM2):
    full_path = os.path.join(directoryM2,item)
    if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        times_M2.append(float(item))
times_M2.sort(key=lambda x: float(x))
times_M2 = times_M2[1:]
data_T_z1_M2, data_U_z1_M2, data_points_z1_M2, T_bulk_z1_M2, data_centroid_z1_M2,data_volumes_z1_M2 = all_functions.temp_points(vtk_directoryM2,params.z1+0.045,times_M2,ratio)
data_T_z2_M2, data_U_z2_M2, data_points_z2_M2, T_bulk_z2_M2, data_centroid_z2_M2,data_volumes_z2_M2 = all_functions.temp_points(vtk_directoryM2,params.z2+0.045,times_M2,ratio)
data_T_z3_M2, data_U_z3_M2, data_points_z3_M2, T_bulk_z3_M2, data_centroid_z3_M2,data_volumes_z3_M2 = all_functions.temp_points(vtk_directoryM2,params.z3+0.045,times_M2,ratio)
ratio_z4 = 0.5
data_T_z4_M2, data_U_z4_M2, data_points_z4_M2, T_bulk_z4_M2, data_centroid_z4_M2,data_volumes_z4_M2 = all_functions.temp_points(vtk_directoryM2,params.z4+0.045,times_M2,ratio_z4)
ratio_z5 = 0.5
data_T_z5_M2, data_U_z5_M2, data_points_z5_M2, T_bulk_z5_M2, data_centroid_z5_M2,data_volumes_z5_M2 = all_functions.temp_points(vtk_directoryM2,params.z5+0.045,times_M2,ratio_z5)
ratio_z6 = 0.5
data_T_z6_M2, data_U_z6_M2, data_points_z6_M2, T_bulk_z6_M2, data_centroid_z6_M2,data_volumes_z6_M2 = all_functions.temp_points(vtk_directoryM2,params.z6+0.045,times_M2,ratio_z6)
ratio_z7 = 0.5
data_T_z7_M2, data_U_z7_M2, data_points_z7_M2, T_bulk_z7_M2, data_centroid_z7_M2,data_volumes_z7_M2 = all_functions.temp_points(vtk_directoryM2,params.z7+0.045,times_M2,ratio_z7)
z1_2,m1_2 = 1*np.ones_like(data_T_z1_M2[-1]),2*np.ones_like(data_T_z1_M2[-1])
z2_2,m2_2 = 2*np.ones_like(data_T_z2_M2[-1]),2*np.ones_like(data_T_z2_M2[-1])
z3_2,m3_2 = 3*np.ones_like(data_T_z3_M2[-1]),2*np.ones_like(data_T_z3_M2[-1])
z4_2,m4_2 = 4*np.ones_like(data_T_z4_M2[-1]),2*np.ones_like(data_T_z4_M2[-1])
z5_2,m5_2 = 5*np.ones_like(data_T_z5_M2[-1]),2*np.ones_like(data_T_z5_M2[-1])
z6_2,m6_2 = 6*np.ones_like(data_T_z6_M2[-1]),2*np.ones_like(data_T_z6_M2[-1])
z7_2,m7_2 = 7*np.ones_like(data_T_z7_M2[-1]),2*np.ones_like(data_T_z7_M2[-1])
print('finished processing Mesh 2')
###############################################
########## Process data for Mesh 2.2 ########## 
###############################################
ratio =  0.75
times_M22 = [0,]
for item in os.listdir(directoryM22):
    full_path = os.path.join(directoryM22,item)
    if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        times_M22.append(float(item))
times_M22.sort(key=lambda x: float(x))
times_M22 = times_M22[1:]
data_T_z1_M22,data_U_z1_M22,data_points_z1_M22,T_bulk_z1_M22,data_centroid_z1_M22,data_volumes_z1_M22=all_functions.temp_points(vtk_directoryM22,params.z1+0.045,times_M22,ratio)
data_T_z2_M22,data_U_z2_M22,data_points_z2_M22,T_bulk_z2_M22,data_centroid_z2_M22,data_volumes_z2_M22=all_functions.temp_points(vtk_directoryM22,params.z2+0.045,times_M22,ratio)
data_T_z3_M22,data_U_z3_M22,data_points_z3_M22,T_bulk_z3_M22,data_centroid_z3_M22,data_volumes_z3_M22=all_functions.temp_points(vtk_directoryM22,params.z3+0.045,times_M22,ratio)
ratio_z4 = 0.5
data_T_z4_M22,data_U_z4_M22,data_points_z4_M22,T_bulk_z4_M22,data_centroid_z4_M22,data_volumes_z4_M22=all_functions.temp_points(vtk_directoryM22,params.z4+0.045,times_M22,ratio_z4)
ratio_z5 = 0.5
data_T_z5_M22,data_U_z5_M22,data_points_z5_M22,T_bulk_z5_M22,data_centroid_z5_M22,data_volumes_z5_M22=all_functions.temp_points(vtk_directoryM22,params.z5+0.045,times_M22,ratio_z5)
ratio_z6 = 0.5
data_T_z6_M22,data_U_z6_M22,data_points_z6_M22,T_bulk_z6_M22,data_centroid_z6_M22,data_volumes_z6_M22=all_functions.temp_points(vtk_directoryM22,params.z6+0.045,times_M22,ratio_z6)
ratio_z7 = 0.5
data_T_z7_M22,data_U_z7_M22,data_points_z7_M22,T_bulk_z7_M22,data_centroid_z7_M22,data_volumes_z7_M22=all_functions.temp_points(vtk_directoryM22,params.z7+0.045,times_M22,ratio_z7)
z1_22,m1_22 = 1*np.ones_like(data_T_z1_M22[-1]),2.2*np.ones_like(data_T_z1_M22[-1])
z2_22,m2_22 = 2*np.ones_like(data_T_z2_M22[-1]),2.2*np.ones_like(data_T_z2_M22[-1])
z3_22,m3_22 = 3*np.ones_like(data_T_z3_M22[-1]),2.2*np.ones_like(data_T_z3_M22[-1])
z4_22,m4_22 = 4*np.ones_like(data_T_z4_M22[-1]),2.2*np.ones_like(data_T_z4_M22[-1])
z5_22,m5_22 = 5*np.ones_like(data_T_z5_M22[-1]),2.2*np.ones_like(data_T_z5_M22[-1])
z6_22,m6_22 = 6*np.ones_like(data_T_z6_M22[-1]),2.2*np.ones_like(data_T_z6_M22[-1])
z7_22,m7_22 = 7*np.ones_like(data_T_z7_M22[-1]),2.2*np.ones_like(data_T_z7_M22[-1])
print('finished processing Mesh 2.2')
###########################################################
#### Convert data_centroid into x,y points and radii ###### 
###########################################################
xM0_all, yM0_all, rM0_all = [],[],[] 
xM1_all, yM1_all, rM1_all = [],[],[]
xM2_all, yM2_all, rM2_all = [],[],[]
xM22_all, yM22_all, rM22_all = [],[],[]
data_centroids_M0 = [data_centroid_z1_M0[-1] ,data_centroid_z2_M0[-1] ,data_centroid_z3_M0[-1],data_centroid_z4_M0[-1],data_centroid_z5_M0[-1],data_centroid_z6_M0[-1],data_centroid_z7_M0[-1]]
data_centroids_M1 = [data_centroid_z1_M1[-1] ,data_centroid_z2_M1[-1] ,data_centroid_z3_M1[-1],data_centroid_z4_M1[-1],data_centroid_z5_M1[-1],data_centroid_z6_M1[-1],data_centroid_z7_M1[-1]]
data_centroids_M2 = [data_centroid_z1_M2[-1] ,data_centroid_z2_M2[-1] ,data_centroid_z3_M2[-1],data_centroid_z4_M2[-1],data_centroid_z5_M2[-1],data_centroid_z6_M2[-1],data_centroid_z7_M2[-1]]
data_centroids_M22 = [data_centroid_z1_M22[-1] ,data_centroid_z2_M22[-1] ,data_centroid_z3_M22[-1],data_centroid_z4_M22[-1],data_centroid_z5_M22[-1],data_centroid_z6_M22[-1],data_centroid_z7_M22[-1]]
# going through all [z1,z2,z3,z4,z5,z6,z7] and generating radii
k = 0
for zs in params.z:
    xM0,yM0 = data_centroids_M0[k][:,0],data_centroids_M0[k][:,1]
    xM1,yM1 = data_centroids_M1[k][:,0],data_centroids_M1[k][:,1]
    xM2,yM2 = data_centroids_M2[k][:,0],data_centroids_M2[k][:,1]
    xM22,yM22 = data_centroids_M22[k][:,0],data_centroids_M22[k][:,1]
    rM0, rM1, rM2, rM22 = np.sqrt(xM0**2 +yM0**2), np.sqrt(xM1**2 +yM1**2),np.sqrt(xM2**2 +yM2**2),np.sqrt(xM22**2 +yM22**2)
    xM0_all.append(xM0)
    yM0_all.append(yM0) 
    xM1_all.append(xM1)
    yM1_all.append(yM1)
    xM2_all.append(xM2)
    yM2_all.append(yM2)
    xM22_all.append(xM22)
    yM22_all.append(yM22)
    rM0_all.append(rM0)
    rM1_all.append(rM1)
    rM2_all.append(rM2)
    rM22_all.append(rM22)
    k +=1
##################################################################
#### Build dataframe for Mesh 0 data (Mesh,z,x,y,r,T,U,Vol) ###### 
##################################################################
data_m0z1 = pd.DataFrame({'Mesh':m1_0,'z':z1_0,'x':xM0_all[0],'y':yM0_all[0],'r':rM0_all[0],
                                'T':data_T_z1_M0[-1],'U':data_U_z1_M0[-1],'Vol':data_volumes_z1_M0[-1]})
data_m0z2 = pd.DataFrame({'Mesh':m2_0,'z':z2_0,'x':xM0_all[1],'y':yM0_all[1],'r':rM0_all[1],
                                'T':data_T_z2_M0[-1],'U':data_U_z2_M0[-1],'Vol':data_volumes_z2_M0[-1]})
data_m0z3 = pd.DataFrame({'Mesh':m3_0,'z':z3_0,'x':xM0_all[2],'y':yM0_all[2],'r':rM0_all[2],
                                'T':data_T_z3_M0[-1],'U':data_U_z3_M0[-1],'Vol':data_volumes_z3_M0[-1]})
data_m0z4 = pd.DataFrame({'Mesh':m4_0,'z':z4_0,'x':xM0_all[3],'y':yM0_all[3],'r':rM0_all[3],
                                'T':data_T_z4_M0[-1],'U':data_U_z4_M0[-1],'Vol':data_volumes_z4_M0[-1]})
data_m0z5 = pd.DataFrame({'Mesh':m5_0,'z':z5_0,'x':xM0_all[4],'y':yM0_all[4],'r':rM0_all[4],
                                'T':data_T_z5_M0[-1],'U':data_U_z5_M0[-1],'Vol':data_volumes_z5_M0[-1]})
data_m0z6 = pd.DataFrame({'Mesh':m6_0,'z':z6_0,'x':xM0_all[5],'y':yM0_all[5],'r':rM0_all[5],
                                'T':data_T_z6_M0[-1],'U':data_U_z6_M0[-1],'Vol':data_volumes_z6_M0[-1]})
data_m0z7 = pd.DataFrame({'Mesh':m7_0,'z':z7_0,'x':xM0_all[6],'y':yM0_all[6],'r':rM0_all[6],
                                'T':data_T_z7_M0[-1],'U':data_U_z7_M0[-1],'Vol':data_volumes_z7_M0[-1]})
data_m0 = pd.concat([data_m0z1, data_m0z2,data_m0z3, data_m0z4,data_m0z5, data_m0z6,data_m0z7])
############################################################################
#### Build dataframe for Mesh 0 Bulk Temperature data (Mesh,z,T_bulk) ###### 
############################################################################
data_Tbulk_m0 = pd.DataFrame({'Mesh':np.zeros_like(params.z),'z':np.arange(1,8,1),
                           'Tbulk_sim':[T_bulk_z1_M0[-1],T_bulk_z2_M0[-1],T_bulk_z3_M0[-1],T_bulk_z4_M0[-1],
                                    T_bulk_z5_M0[-1],T_bulk_z6_M0[-1],T_bulk_z7_M0[-1]]})
##################################################################
#### Build dataframe for Mesh 1 data (Mesh,z,x,y,r,T,U,Vol) ###### 
##################################################################
data_m1z1 = pd.DataFrame({'Mesh':m1_1,'z':z1_1,'x':xM1_all[0],'y':yM1_all[0],'r':rM1_all[0],
                                'T':data_T_z1_M1[-1],'U':data_U_z1_M1[-1],'Vol':data_volumes_z1_M1[-1]})
data_m1z2 = pd.DataFrame({'Mesh':m2_1,'z':z2_1,'x':xM1_all[1],'y':yM1_all[1],'r':rM1_all[1],
                                'T':data_T_z2_M1[-1],'U':data_U_z2_M1[-1],'Vol':data_volumes_z2_M1[-1]})
data_m1z3 = pd.DataFrame({'Mesh':m3_1,'z':z3_1,'x':xM1_all[2],'y':yM1_all[2],'r':rM1_all[2],
                                'T':data_T_z3_M1[-1],'U':data_U_z3_M1[-1],'Vol':data_volumes_z3_M1[-1]})
data_m1z4 = pd.DataFrame({'Mesh':m4_1,'z':z4_1,'x':xM1_all[3],'y':yM1_all[3],'r':rM1_all[3],
                                'T':data_T_z4_M1[-1],'U':data_U_z4_M1[-1],'Vol':data_volumes_z4_M1[-1]})
data_m1z5 = pd.DataFrame({'Mesh':m5_1,'z':z5_1,'x':xM1_all[4],'y':yM1_all[4],'r':rM1_all[4],
                                'T':data_T_z5_M1[-1],'U':data_U_z5_M1[-1],'Vol':data_volumes_z5_M1[-1]})
data_m1z6 = pd.DataFrame({'Mesh':m6_1,'z':z6_1,'x':xM1_all[5],'y':yM1_all[5],'r':rM1_all[5],
                                'T':data_T_z6_M1[-1],'U':data_U_z6_M1[-1],'Vol':data_volumes_z6_M1[-1]})
data_m1z7 = pd.DataFrame({'Mesh':m7_1,'z':z7_1,'x':xM1_all[6],'y':yM1_all[6],'r':rM1_all[6],
                                'T':data_T_z7_M1[-1],'U':data_U_z7_M1[-1],'Vol':data_volumes_z7_M1[-1]})
data_m1 = pd.concat([data_m1z1, data_m1z2,data_m1z3, data_m1z4,data_m1z5, data_m1z6,data_m1z7])
############################################################################
#### Build dataframe for Mesh 1 Bulk Temperature data (Mesh,z,T_bulk) ###### 
############################################################################
data_Tbulk_m1 = pd.DataFrame({'Mesh':np.ones_like(params.z),'z':np.arange(1,8,1),
                           'Tbulk_sim':[T_bulk_z1_M1[-1],T_bulk_z2_M1[-1],T_bulk_z3_M1[-1],T_bulk_z4_M1[-1],
                                    T_bulk_z5_M1[-1],T_bulk_z6_M1[-1],T_bulk_z7_M1[-1]]})
##################################################################
#### Build dataframe for Mesh 2 data (Mesh,z,x,y,r,T,U,Vol) ###### 
##################################################################
data_m2z1 = pd.DataFrame({'Mesh':m1_2,'z':z1_2,'x':xM2_all[0],'y':yM2_all[0],'r':rM2_all[0],
                                'T':data_T_z1_M2[-1],'U':data_U_z1_M2[-1],'Vol':data_volumes_z1_M2[-1]})
data_m2z2 = pd.DataFrame({'Mesh':m2_2,'z':z2_2,'x':xM2_all[1],'y':yM2_all[1],'r':rM2_all[1],
                                'T':data_T_z2_M2[-1],'U':data_U_z2_M2[-1],'Vol':data_volumes_z2_M2[-1]})
data_m2z3 = pd.DataFrame({'Mesh':m3_2,'z':z3_2,'x':xM2_all[2],'y':yM2_all[2],'r':rM2_all[2],
                                'T':data_T_z3_M2[-1],'U':data_U_z3_M2[-1],'Vol':data_volumes_z3_M2[-1]})
data_m2z4 = pd.DataFrame({'Mesh':m4_2,'z':z4_2,'x':xM2_all[3],'y':yM2_all[3],'r':rM2_all[3],
                                'T':data_T_z4_M2[-1],'U':data_U_z4_M2[-1],'Vol':data_volumes_z4_M2[-1]})
data_m2z5 = pd.DataFrame({'Mesh':m5_2,'z':z5_2,'x':xM2_all[4],'y':yM2_all[4],'r':rM2_all[4],
                                'T':data_T_z5_M2[-1],'U':data_U_z5_M2[-1],'Vol':data_volumes_z5_M2[-1]})
data_m2z6 = pd.DataFrame({'Mesh':m6_2,'z':z6_2,'x':xM2_all[5],'y':yM2_all[5],'r':rM2_all[5],
                                'T':data_T_z6_M2[-1],'U':data_U_z6_M2[-1],'Vol':data_volumes_z6_M2[-1]})
data_m2z7 = pd.DataFrame({'Mesh':m7_2,'z':z7_2,'x':xM2_all[6],'y':yM2_all[6],'r':rM2_all[6],
                                'T':data_T_z7_M2[-1],'U':data_U_z7_M2[-1],'Vol':data_volumes_z7_M2[-1]})
data_m2 = pd.concat([data_m2z1, data_m2z2,data_m2z3, data_m2z4,data_m2z5, data_m2z6,data_m2z7])
############################################################################
#### Build dataframe for Mesh 2 Bulk Temperature data (Mesh,z,T_bulk) ###### 
############################################################################
data_Tbulk_m2 = pd.DataFrame({'Mesh':2*np.ones_like(params.z),'z':np.arange(1,8,1),
                           'Tbulk_sim':[T_bulk_z1_M2[-1],T_bulk_z2_M2[-1],T_bulk_z3_M2[-1],T_bulk_z4_M2[-1],
                                    T_bulk_z5_M2[-1],T_bulk_z6_M2[-1],T_bulk_z7_M2[-1]]})

####################################################################
#### Build dataframe for Mesh 2.2 data (Mesh,z,x,y,r,T,U,Vol) ###### 
####################################################################
data_m22z1 = pd.DataFrame({'Mesh':m1_22,'z':z1_22,'x':xM22_all[0],'y':yM22_all[0],'r':rM22_all[0],
                                'T':data_T_z1_M22[-1],'U':data_U_z1_M22[-1],'Vol':data_volumes_z1_M22[-1]})
data_m22z2 = pd.DataFrame({'Mesh':m2_22,'z':z2_22,'x':xM22_all[1],'y':yM22_all[1],'r':rM22_all[1],
                                'T':data_T_z2_M22[-1],'U':data_U_z2_M22[-1],'Vol':data_volumes_z2_M22[-1]})
data_m22z3 = pd.DataFrame({'Mesh':m3_22,'z':z3_22,'x':xM22_all[2],'y':yM22_all[2],'r':rM22_all[2],
                                'T':data_T_z3_M22[-1],'U':data_U_z3_M22[-1],'Vol':data_volumes_z3_M22[-1]})
data_m22z4 = pd.DataFrame({'Mesh':m4_22,'z':z4_22,'x':xM22_all[3],'y':yM22_all[3],'r':rM22_all[3],
                                'T':data_T_z4_M22[-1],'U':data_U_z4_M22[-1],'Vol':data_volumes_z4_M22[-1]})
data_m22z5 = pd.DataFrame({'Mesh':m5_22,'z':z5_22,'x':xM22_all[4],'y':yM22_all[4],'r':rM22_all[4],
                                'T':data_T_z5_M22[-1],'U':data_U_z5_M22[-1],'Vol':data_volumes_z5_M22[-1]})
data_m22z6 = pd.DataFrame({'Mesh':m6_22,'z':z6_22,'x':xM22_all[5],'y':yM22_all[5],'r':rM22_all[5],
                                'T':data_T_z6_M22[-1],'U':data_U_z6_M22[-1],'Vol':data_volumes_z6_M22[-1]})
data_m22z7 = pd.DataFrame({'Mesh':m7_22,'z':z7_22,'x':xM22_all[6],'y':yM22_all[6],'r':rM22_all[6],
                                'T':data_T_z7_M22[-1],'U':data_U_z7_M22[-1],'Vol':data_volumes_z7_M22[-1]})
data_m22 = pd.concat([data_m22z1, data_m22z2,data_m22z3, data_m22z4,data_m22z5, data_m22z6,data_m22z7])
############################################################################
#### Build dataframe for Mesh 2 Bulk Temperature data (Mesh,z,T_bulk) ###### 
############################################################################
data_Tbulk_m22 = pd.DataFrame({'Mesh':2.2*np.ones_like(params.z),'z':np.arange(1,8,1),
                           'Tbulk_sim':[T_bulk_z1_M22[-1],T_bulk_z2_M22[-1],T_bulk_z3_M22[-1],T_bulk_z4_M22[-1],
                                    T_bulk_z5_M22[-1],T_bulk_z6_M22[-1],T_bulk_z7_M22[-1]]})

##################################################
###### Check that the total concatenated sums are correct!!!!
##################################################
sum_parts = len(data_m2z1)+len(data_m2z2)+len(data_m2z3)+len(data_m2z4)+len(data_m2z5)+len(data_m2z6)+len(data_m2z7)
total_parts= len(data_m2)
#print(f'total_parts={total_parts} = sum_parts={sum_parts}')

##################################################
###### Combine all mesh dataframes
##################################################
data_mAll = pd.concat([data_m0,data_m1,data_m2,data_m22])
data_Tbulk_mAll = pd.concat([data_Tbulk_m0,data_Tbulk_m1,data_Tbulk_m2,data_Tbulk_m22])
##################################################
###### Save to a csv file one directory above
##################################################
data_mAll.to_csv('../data/data_mAll.csv',index=False)
data_Tbulk_mAll.to_csv('../data/dataTbulk_mAll.csv',index=False)
