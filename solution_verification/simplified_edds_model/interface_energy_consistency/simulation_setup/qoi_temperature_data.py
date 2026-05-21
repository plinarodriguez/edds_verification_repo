#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import pyvista as pv
import pandas as pd
import re

def temp_points(workdir,points):
    ########### Collect times from directory (workdir = path)
    times = [0,]
    for item in os.listdir(workdir):
        full_path = os.path.join(workdir,item)
#        print(f'full_path ={full_path}')
#        if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        if os.path.isdir(workdir) and item[0:].replace('.','').isdigit():
#            print(f'full_path ={full_path}')
            times.append(float(item))
#    print(f'times {times}')
    times.sort(key=lambda x: float(x)) # sort the time values
    times = np.array(times[1:]) # removes 0 value,Openfoam config initial values
    times = np.around(times,2)  # round the values to a single decimal point
    directory_path_fluid = workdir+'/VTK/pipeFluid'  
    directory_path_solid = workdir+'/VTK/caseSolid'
    ########### Convert VTK file label(iteration #) with Time instead
    for filename in os.listdir(directory_path_fluid):
        # go through all files with vtk extention
        if filename.endswith('.vtk'):
            match = re.search(r'_(\d+)\.vtk$',filename) # collect file number name (number.vtk)
            if match: # if a number exists (Truthiness)
                number = match.group(1)  # save the number 
                padded_number = number.zfill(9)  # add zeros infront of number so that they can be sorted correctly
                new_filename = filename.replace(f'_{number}.vtk',f'_{padded_number}.vtk') # create new file name with padded number
                old_path = os.path.join(directory_path_fluid,filename) 
                new_path = os.path.join(directory_path_fluid,new_filename)
                os.rename(old_path,new_path) # replace the old file name with the new
    ########## Sort the renamed vtk files
    vtk_files = sorted([f for f in os.listdir(directory_path_fluid) if f.endswith(".vtk")])
    ########## Initialize mesh dataset with dimensions of points
    point_cloud = pv.PolyData(points)
    data = []
    # for each vtk time file 
    for file in vtk_files:
        dataset = pv.read(directory_path_fluid+'/'+file) #reads vtk file and extracts data
        sampled_point = point_cloud.sample(dataset)      # sample points from dataset
        temperatures = sampled_point.point_data['T']     # collect Temperature@ sample points
        data.append(temperatures) 
    data = np.array(data)
    return data,times 

def temp_points_Tavg(workdir,points,z):
    ########### Collect times from directory (workdir = path)
    times = [0,]
    for item in os.listdir(workdir):
        full_path = os.path.join(workdir,item)
#        print(f'full_path ={full_path}')
#        if os.path.isdir(item) and item[0:].replace('.','').isdigit():
        if os.path.isdir(workdir) and item[0:].replace('.','').isdigit():
#            print(f'full_path ={full_path}')
            times.append(float(item))
#    print(f'times {times}')
    times.sort(key=lambda x: float(x)) # sort the time values
    times = np.array(times[1:]) # removes 0 value,Openfoam config initial values
    times = np.around(times,2)  # round the values to a single decimal point
    directory_path_fluid = workdir+'/VTK/pipeFluid'
    directory_path_solid = workdir+'/VTK/caseSolid'
    ########### Convert VTK file label(iteration #) with Time instead
    for filename in os.listdir(directory_path_fluid):
        # go through all files with vtk extention
        if filename.endswith('.vtk'):
            match = re.search(r'_(\d+)\.vtk$',filename) # collect file number name (number.vtk)
            if match: # if a number exists (Truthiness)
                number = match.group(1)  # save the number 
                padded_number = number.zfill(10)  # add zeros infront of number so that they can be sorted correctly
                new_filename = filename.replace(f'_{number}.vtk',f'_{padded_number}.vtk') # create new file name with padded number
                old_path = os.path.join(directory_path_fluid,filename)
                new_path = os.path.join(directory_path_fluid,new_filename)
                os.rename(old_path,new_path) # replace the old file name with the new
    ########## Sort the renamed vtk files
    vtk_files = sorted([f for f in os.listdir(directory_path_fluid) if f.endswith(".vtk")])
    ########## Initialize mesh dataset with dimensions of points
    point_cloud = pv.PolyData(points)
     # Initialize lists to store results over time 
    data_T = []      # Temperature data at each time step 
    T_avg = []      # Bulk temperatures at each time step    
    for file in vtk_files:
        dataset = pv.read(directory_path_fluid+'/'+file) #reads vtk file and extracts data
        # Compute cell centers and extract points 
        cell_centers = dataset.cell_centers()
        centroids = cell_centers.points # shape is (n_cells, 3)
        dz_estimate = np.mean(np.diff(np.sort(np.unique(centroids[:,2]))))
        if workdir == 'workdir.1':
            tol = 3.6e-4
        elif workdir == 'workdir.2':
            tol = 2.8e-4
        elif workdir == 'workdir.3':
            tol = 2.2e-4 #ratio*dz_estimate # based on representative length
        elif workdir == 'workdir.4':
            tol = 1.7e-4
        elif workdir == 'workdir.5':
            tol = 1.3e-4
        elif workdir == 'workdir.6':
            tol = 1.0e-4
        elif workdir == 'workdir.7':
            tol = 0.8e-4
        #tol =2.2e-4 #1.2e-4  # choose this based on representative length
        # Select cells whose centroid z-value is near the target z
        range_nearZ = np.abs(centroids[:,2]-z) < tol
        selected_cell_ids = np.where(range_nearZ)[0]
#         print(f'{file}: {len(selected_cell_ids)} cells seleccted at z={z}')
        # Compute Cell Volumes
        mesh = dataset.compute_cell_sizes(length=False, area=False, volume=True)
        volumes = mesh.cell_data['Volume']

        selected_T = []
        selected_points = []
        selected_volumes = []

        for cell_id in selected_cell_ids:
            cell = mesh.extract_cells(cell_id)
            cell_vol = volumes[cell_id]
            # Get point indices for this cell
            points = centroids[cell_id]
            T_vals = mesh.cell_data['T'][cell_id]
            selected_points.extend(points)
            selected_T.extend([T_vals])
            selected_volumes.extend([cell_vol])
        selected_T = np.array(selected_T)
        selected_volumes = np.array(selected_volumes)

        numerator = np.sum(selected_T*selected_volumes)
        denominator = np.sum(selected_volumes)
        if denominator == 0:
            print(f'There was an error in selected volumes = {denominator}')
        else: 
            t_b = numerator /denominator    
        data_T.append(selected_T)
        T_avg.append(t_b)

    # Convert results to numpy arrays for easy processing downstream
    data_T = np.array(data_T)
    T_avg = np.array(T_avg)
    return T_avg,times

def data_qoi(target_times,vtk_directory,points,zs,Tavg):
  # points = np.array(points)
#   print(points)
   if Tavg == True:
       data,times = temp_points_Tavg(vtk_directory,points,zs)   # call function to collect temperature and times
   else:
       data,times = temp_points(vtk_directory,points)   # call function to collect temperature and times 
   test_time = times
 #   print(f'test_time = {test_time}')
   rounded_list = [round(num, 5) for num in test_time]
   test1 = pd.DataFrame({'col1': test_time, 'col2': rounded_list})
   target_index = []
   target_temp = []
#   print(f'data')
  #  print(f'target_times:{target_times}')
  #  print(f'rounded_list:{rounded_list}')
   #for i in target_times:
   index_of_number = rounded_list.index(target_times)  
   target_index.append(index_of_number)
#   target_temp.append(data[index_of_number,:].tolist())
   target_temp.append(data[index_of_number].tolist())
   test_temper = np.array(target_temp)
   return test_temper


if __name__ == "__main__":
    #vtk_directory = 'VTK/'
    #points = [[0,0,0.001],[0,0,0.006],[0,0.0,0.030],[0,0.000,0.045],[0,0.000,0.0517],
    #          [0,0.001,0.006],[0,0.002,0.006],[0,0.00225,0.006],
    #          [0,0.001,0.030],[0,0.002,0.030],[0,0.00225,0.030],
    #          [0,0.001,0.0517],[0,0.002,0.0517],[0,0.00225,0.0517],
    #          [0,0.001,0.0],[0,0.002,0.0],[0,0.00225,0.0]]
    
    #data,time = temp_points(vtk_directory,points)
#    target_times = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
    qois = data_qoi(target_times,vtk_directory,points)

