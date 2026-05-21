#### This function (temp_points) is modified for temperature in solid only not the fluid
#### Might also not need all these other functions. But clean up later. 

#Functions
import numpy as np
import os
import re
import pyvista as pv

def temp_points(vtk_directory,z,time_steps, ratio):
    """
    Extract temperature and velocity magnitude data at a plane slice z-location from a series of VTK files 
    in a specified directory
    
    PARAMETERS
    vtk_directory : str
        The path to the directory containing the VTK files
    z : float
        The z-coordinate to extract the slice
    time_steps : list 
        A list of time step identifiers, though it is not used directly in the code 
        
    RETURNS
    data_T : np.ndarray
        Array of temperature values at the slice plane for each time step
    data_points : list 
        List of arrays of coordinates (x,y,z) for each point in the slice
    """
    # Define paths to the VTK directories
    directory_path_solid = vtk_directory+'/caseSolid'
    
    # Loop through all files in the solid VTK directory
    for filename in os.listdir(directory_path_solid):
        if filename.endswith('.vtk'):
            # Use regular expression to extract timestep number (ex: _1.vtk)
            match = re.search(r'_(\d+)\.vtk$',filename)
            if match:
                number = match.group(1)         # Extract number from match
                padded_number = number.zfill(6) # Pad the number with leading zeros to 2 digits
                new_filename = filename.replace(f'_{number}.vtk',f'_{padded_number}.vtk')
                # Rename the file to have consistent naming (ex: _01.vtk)
                old_path = os.path.join(directory_path_solid,filename)
                new_path = os.path.join(directory_path_solid,new_filename)
                os.rename(old_path,new_path)
                
    # Get sorted list of all VTK files in the solid directory 
    vtk_files = sorted([f for f in os.listdir(directory_path_solid) if f.endswith(".vtk")])
    # Initialize lists to store results over time 
    data_T = []      # Temperature data at each time step 
    data_points = [] # Coordinates of points on the slice at each time step  
    data_centroids = []
    data_volumes = [] 
    # Loop through each VTK file that is already in order 
    for file in vtk_files:
        # Read the VTK file using PyVista
        dataset = pv.read(directory_path_solid+'/'+file)
        # Compute cell centers and extract points 
        cell_centers = dataset.cell_centers()
        centroids = cell_centers.points # shape is (n_cells, 3)
        dz_estimate = np.mean(np.diff(np.sort(np.unique(centroids[:,2]))))
        tol = ratio*dz_estimate
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
        data_points.append(np.array(selected_points))
        selected_centroids = np.reshape(selected_points, (-1,3))
        data_centroids.append(selected_centroids)
        data_volumes.append(np.array(selected_volumes))
        data_T.append(selected_T)
        
    # Convert results to numpy arrays for easy processing downstream     
    data_T = np.array(data_T)        
    return data_T, data_points, data_centroids,data_volumes
