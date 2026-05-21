# Reproducible Verification Studies for a Multiphysics EDDS Model

This repository contains reproducible code and solution verification studies for a simplified electronic drug delivery system (EDDS) modeled using OpenFOAM.

The project includes:

* Code verification using analytical solutions
* Solution verification using StREEQ
* Automated HPC workflows using SLURM and Dakota
* Parallel OpenFOAM simulations using MPI
* Python-based post-processing and verification analysis

The workflows are designed to support transparent and reproducible computational modeling and simulation (CM&S) studies for credibility assessment.

---

# Scientific Motivation

The full EDDS multiphysics system does not have an analytical solution. To build credibility in the computational model, verification studies were performed using simplified geometries and isolated physics.

The verification strategy follows a modular approach:

1. Isolate individual physics
2. Compare against analytical solutions when possible
3. Quantify discretization error
4. Assess convergence behavior
5. Evaluate coupled multiphysics behavior

This repository supports reproducible verification workflows aligned with risk-informed credibility assessment approaches for computational modeling and simulation.

---

# Computational Model

## Physical System

A physics-based computational model was developed for an electronic drug delivery system (EDDS). The system consists of:

* Fluid flow through a pipe
* Heat transfer through a surrounding solid casing
* Conjugate heat transfer between the fluid and solid regions
* Transient thermal behavior

Fluid enters through the inlet region, passes through a heated casing section, and exits through the outlet region.

## Governing Physics

The model includes:

* Incompressible laminar fluid flow
* Heat conduction within the solid casing
* Conjugate heat transfer at the fluid-solid interface
* Transient thermal diffusion

## Numerical Solver

The simulations use:

* OpenFOAM v9
* `chtMultiRegionFoam`
* MPI-based parallelization
* SLURM job scheduling on HPC systems

## Mesh Generation

Meshes were generated using Cubit and exported as Fluent `.msh` files before conversion to OpenFOAM format.

Meshes are not included directly in the repository. Instead, Cubit journal files are provided to support reproducible mesh generation.

---

# Repository Organization

```text
├── code_verification/
│   ├── hydrodynamic_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   ├── radial_conduction_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   └── thermal_diffusion_model/
│       ├── analysis/
│       ├── mesh/
│       └── simulation_setup/
│
├── solution_verification/
│   ├── coupled_pipe_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   └── simplified_edds_model/
│       ├── co_refinement_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   ├── cost_study/
│       │   └── simulation_setup/
│       │
│       ├── interface_energy_consistency/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       ├── solver_tolerance_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       ├── spatial_refinement_only_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       └── temporal_refinement_only_study/
│           ├── analysis/
│           ├── mesh/
│           └── simulation_setup/
```

---

# Software Requirements

## Required Software

* OpenFOAM v9
* Python 3.x
* MPI
* SLURM
* Cubit
* Dakota
* StREEQ

## Python Packages

* numpy
* pandas
* matplotlib
* pyvista

## HPC Assumptions

The workflows assume:

* Access to a SLURM-managed HPC cluster
* MPI-enabled OpenFOAM installation
* Parallel job submission capability

---

# Reproducibility Notes

This repository is designed to support reproducible computational modeling and simulation workflows.

Reproducibility considerations include:

* Version-controlled simulation setup files
* Automated workflow execution
* Scripted mesh generation
* Automated post-processing
* Explicit software dependency tracking
* Structured verification studies

Meshes are generated using Cubit journal files to allow reproducible reconstruction of the computational domains.

Large simulation outputs are reduced through extraction of quantities of interest (QoIs) into CSV files for lightweight post-processing and analysis.

---

# Running the Workflows

## Single Simulation Studies

Single simulation studies include:

* Hydrodynamic model
* Radial conduction model
* Thermal diffusion model
* Coupled pipe model

These workflows:

* Run a single OpenFOAM simulation
* Use MPI mesh decomposition for parallel execution
* Reconstruct decomposed solutions after simulation completion

### Example Execution

```bash
sbatch sbatch.batch
```

### Workflow Summary

1. Generate mesh
2. Decompose domain
3. Run OpenFOAM simulation
4. Reconstruct solution
5. Extract quantities of interest from VTK files 
6. Run verification post-processing

---

## Multiple Simulation Studies

Multiple simulation studies include:

* Co-refinement study
* Solver tolerance study
* Spatial refinement study
* Temporal refinement study
* Interface consistency study

These workflows:

* Run multiple simulations simultaneously
* Use Dakota for workflow orchestration
* Use StREEQ for extrapolation and convergence analysis

### Workflow Summary

1. Generate parameterized simulation inputs using dakota input file
2. Submit multiple simulations to run in parallel
3. Extract QoIs from VTK files 
4. Generate extrapolated solutions using StREEQ
5. Compute discretization errors
6. Generate convergence plots

---

# Quantities of Interest (QoIs)

The verification studies use extracted quantities of interest (QoIs) to reduce storage requirements and simplify post-processing.

Typical QoIs include:

* Radial velocity profiles
* Radial temperature profiles
* Interface heat flux
* Transient bulk temperatures

QoIs are extracted from simulation outputs and stored as CSV files for post-processing.

---

# Error Metrics

The repository includes verification analyses using:

* $L_2$ norm error
* Relative error comparisons with extrapolated quantities
* Observed order of convergence

---

# Verification Studies

# Code Verification

Code verification studies compare numerical solutions against analytical solutions using simplified geometries and isolated physics models.

## Hydrodynamic Verification

### Study Goal

Verify the fluid flow solution using the analytical Hagen-Poiseuille velocity profile.

### Physics Assumptions

* Fully developed flow
* Laminar flow
* Newtonian fluid
* Steady-state conditions

### Quantity of Interest

* Radial velocity profile

### Verification Method

Comparison against the Hagen-Poiseuille analytical solution.

---

## Radial Conduction Verification

### Study Goal

Verify the solid heat conduction solution using an analytical radial temperature profile.

### Physics Assumptions

* Steady-state conduction
* Radial heat transfer
* Solid-only conduction

### Quantity of Interest

* Radial temperature profile within the solid

### Verification Method

Comparison against the analytical radial conduction solution.

---

## Transient Thermal Diffusion Verification

### Study Goal

Verify transient thermal diffusion behavior in the fluid region.

### Physics Assumptions

* Zero fluid velocity
* Constant solid temperature
* Transient diffusion-dominated transport

### Quantity of Interest

* Time-dependent fluid temperature profile

### Verification Method

Comparison against an analytical separation-of-variables solution involving Bessel functions.

---

# Solution Verification

Solution verification studies assess discretization error and numerical convergence behavior for the coupled multiphysics system.

## Coupled Pipe Study

### Study Goal

Assess spatial discretization behavior in the coupled heated pipe system.

### Verification Method

StREEQ extrapolation using mesh refinement studies.

---

## Solver Tolerance Study

### Study Goal

Assess sensitivity to solver tolerances.

### Method

* Fixed mesh resolution
* Fixed timestep
* Multiple solver tolerances

---

## Co-Refinement Study

### Study Goal

Assess simultaneous spatial and temporal refinement behavior.

### Method

* Mesh refinement
* Timestep refinement
* Coupled refinement analysis

### Verification Method

Multi-variable StREEQ extrapolation.

---

## Interface Energy Consistency Study

### Study Goal

Assess consistency across the fluid-solid interface.

### Quantities Evaluated

* Temperature continuity
* Temperature gradient consistency
* Interface heat flux consistency

---

## Spatial Refinement Study

### Study Goal

Assess spatial discretization error independently.

### Method

* Fixed timestep
* Mesh refinement only

### Verification Method

StREEQ extrapolation.

---

## Temporal Refinement Study

### Study Goal

Assess temporal discretization error independently.

### Method

* Fixed mesh
* Timestep refinement only

### Verification Method

StREEQ extrapolation.

---

# HPC Workflow

## MPI Parallelization

OpenFOAM simulations are parallelized using MPI decomposition.

Typical workflow:

1. Decompose mesh
2. Run parallel simulation
3. Reconstruct decomposed results

## Dakota Workflow Management

Dakota is used to:

* Generate parameterized studies
* Manage multiple simulations
* Automate job submission
* Coordinate refinement studies

## StREEQ Integration

StREEQ is used for:

* Extrapolated solution estimation
* Observed order of convergence
* Relative error analysis

Repository:
[https://github.com/sandialabs/StREEQ](https://github.com/sandialabs/StREEQ)

---

# References

## Software

* OpenFOAM
* Dakota
* StREEQ
* Cubit

## Standards and Methodology

* ASME V&V 20
* ASME V&V 40
* NASEM Reproducibility and Replicability in Science

## Related Repositories

* StREEQ: [https://github.com/sandialabs/StREEQ](https://github.com/sandialabs/StREEQ)
* EDDS Credibility Plan: [https://github.com/plinarodriguez/edds-credibility-plan](https://github.com/plinarodriguez/edds-credibility-plan)

---

# Citation

If you use this repository in published work, please cite the associated publications and repositories.


