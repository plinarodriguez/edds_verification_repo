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
