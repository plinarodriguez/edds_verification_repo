# Running the OpenFOAM Case (Single-Case Template)

This directory is a **single-case OpenFOAM run template**. OpenFOAM requires a specific directory structure and configuration files (e.g., `0/`, `constant/`, `system/`) in order to run a simulation. The provided `sbatch` script creates those directories, copies the required configuration files from the `template/` directory, converts the mesh, decomposes the case for parallel execution, runs the solver, reconstructs results, and writes VTK output.

## Parallel decomposition (decomposeParDict)

This case is designed to run in parallel using OpenFOAM domain decomposition. The decomposition is controlled by `system/decomposeParDict` (and, for multi-region cases, additional `decomposeParDict` files may exist under `system/<regionName>/`). Note that `decomposePar` will create 12 regions (`numberOfSubdomains 12`) to run in parallel in a separate directory named `processor#`.

## Prerequisites
- OpenFOAM-9 environment available on the cluster
- MPI available for parallel runs
- ParaView/`paraFoam` is optional and may require running on a visualization node (or omit/comment out in batch jobs)

## Parallel settings
The number of MPI ranks is set by the Slurm submission options (e.g., `--ntasks`) and must be consistent with `system/decomposeParDict`.

## Cluster / OpenFOAM notes

- This workflow is set up for **OpenFOAM-9**, chosen for cluster compatibility and configuration.
- This case uses the OpenFOAM conjugate heat transfer multi-region solver **`chtMultiRegionFoam`**.
- The top of `sbatch.bash` is intended for **cluster-specific settings**, including module loads (if needed) and OpenFOAM install paths.
- This script is intended to run **one case** at a time (single model configuration).

## Mesh workflow

Meshes are generated in **Cubit** and exported as **Fluent `.msh`** files. The `.msh` file is placed in the case directory and converted to an OpenFOAM mesh at run time using:

- `fluent3DMeshToFoam <mesh_name>.msh`

After conversion, the case is split into regions using:

- `splitMeshRegions -cellZones -overwrite`


## Required manual edit: *mesh filename*

You must edit the mesh conversion line in `sbatch.bash` and replace:

- `mesh_file_name_here.msh`

with your actual mesh filename, for example:

```bash
fluent3DMeshToFoam shortPipelongCase_m0.msh
```

## Parallel decomposition and reconstruction

This case is intended to run in parallel with OpenFOAM domain decomposition:

1. **Decompose (pre-processing)**  
   The script partitions the mesh for parallel execution:
   - `decomposePar -allRegions`  
   This creates `processor*/` subdirectories for each region.

2. **Run in parallel**  
   The solver is launched using:
   - `runParallel $(getApplication)`

3. **Reconstruct (post-processing)**  
   After the run completes, fields are reconstructed back onto the original (non-decomposed) case:
   - `reconstructPar -allRegions`

## What you need in the same directory

Place the following **in the same folder**:

- `sbatch.bash` (the job script below)
- `template/` (contains OpenFOAM dictionaries and region subdirectories)
- the mesh file (e.g., `something.msh`)

### Directory Structure Example
    ```
    radial_conduction_model/
    ├── sbatch.bash
    ├── mesh0.msh
    ├── template/
    │   ├── 0
    │   │   ├── caseSolid
    │   │       ├── cellToRegion
    │   │       ├── T
    │   │   ├── pipeFluid
    │   │       ├── cellToRegion
    │   │       ├── T
    │   │       ├── U
    │   │       ├── p_rgh
    │   │       ├── p
    │   │   ├── cellToRegion
    │   ├── constant
    │   │   ├── caseSolid
    │   │       ├── polyMesh
    │   │            ├── boundary 
    │   │            ├── boundaryRegionAddressing 
    │   │            ├── cellRegionAddressing 
    │   │            ├── cellZones
    │   │            ├── faceRegionAddressing 
    │   │            ├── faces 
    │   │            ├── faceZones  
    │   │            ├── neighbour
    │   │            ├── owner
    │   │            ├── pointRegionAddressing 
    │   │            ├── points
    │   │            ├── pointZones
    │   │       ├── radiationProperties
    │   │       ├── thermophysicalProperties
    │   │   ├── pipeFluid
    │   │       ├── polyMesh
    │   │            ├── boundary 
    │   │            ├── boundaryRegionAddressing 
    │   │            ├── cellRegionAddressing 
    │   │            ├── cellZones
    │   │            ├── faceRegionAddressing 
    │   │            ├── faces 
    │   │            ├── faceZones  
    │   │            ├── neighbour
    │   │            ├── owner
    │   │            ├── pointRegionAddressing 
    │   │            ├── points
    │   │            ├── pointZones
    │   │       ├── radiationProperties
    │   │       ├── thermophysicalProperties
    │   │       ├── momentumTransport
    │   │       ├── turbulenceProperties
    │   │       ├── g
    │   │   ├── polyMesh
    │   │            ├── boundary 
    │   │            ├── boundaryRegionAddressing 
    │   │            ├── cellRegionAddressing 
    │   │            ├── cellZones
    │   │            ├── faceRegionAddressing 
    │   │            ├── faces 
    │   │            ├── faceZones  
    │   │            ├── neighbour
    │   │            ├── owner
    │   │            ├── pointRegionAddressing 
    │   │            ├── points
    │   │            ├── pointZones
    │   │   ├── cellToRegion
    │   │   └── regionProperties
    │   ├── system
    │   │   ├── caseSolid
    │   │       ├── decomposeParDict
    │   │       ├── fvSchemes
    │   │       ├── fvSolution
    │   │       ├── topoSetDict
    │   │   ├── pipeFluid
    │   │       ├── decomposeParDict
    │   │       ├── fvSchemes
    │   │       ├── fvSolution
    │   ├── controlDict
    │   ├── decomposeParDict
    │   ├── fvSchemes
    │   ├── fvSolution
    │   ├── meshQualityDict
    └── README.md

    ```

## Outputs

### OpenFOAM runtime outputs
During the run, OpenFOAM writes solution fields to standard time directories (e.g., `0.1/`, `0.2/`, …) for each region in this multi-region case (e.g., `pipeFluid/`, `caseSolid/`). If the case is run in parallel, intermediate results are written in decomposed form under `processor*/` directories until reconstruction is performed.

### Reconstructed fields
At the end of the job, the script reconstructs all regions: `reconstructPar -allRegions`. After reconstruction, the primary fields will be available in the main case time directories (not only under `processor*/`).

### VTK outputs (for visualization / post-processing)
The script converts results to VTK format for **each region and each written time step** using `foamToVTK`. This produces a `VTK/` directory containing per-time-step VTK output for each region. These VTK files can be used for visualization in ParaView and for downstream post-processing. Note that the VTK output size can grow quickly because it is written for every output time step for each region.