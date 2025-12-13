# Eschallot: Comprehensive Package for the Simulation and Optimization of Spherical Particles

![](logo.png)

Eschallot is an optimization and simulation tool for light scattering by stratified spherical nano-and microparticles, inspired by the needle optimization algorithm used for multilayer thin-film design **[1-3]**. The algorithm alternates between **(a) Shape Optimization** (optimizing the layer boundary positions by gradient descent) and **(b) Topology Nucleation** (optimizing the materials and the number of layers by nucleating an infinitesimal layer at an optimal location) to minimize a user-defined cost function based on the particle's far-field scattering quantities (cross-sections, phase function, etc.). These quantities are computed in each iteration using the transfer matrix method formulation of Mie scattering for multi-shell particles **[4-5]**.

![](flowchart.png)

**If you have found this package helpful in your research, please cite this [work](https://doi.org/10.1016/j.cpc.2025.109966):**

```bibtex
@article{min2025eschallot,
    title={Eschallot: A topology nucleation algorithm for designing stratified, spherically symmetric systems that exhibit complex angular scattering of electromagnetic waves},
    author={Seokhwan Min, Jonghwa Shin},
    journal={Comput. Phys. Commun.},
    volume={},
    number={},
    pages={},
    year={2025}
}
```

**References:**

**[1]** A. V. Tikhonravov, M. K. Trubetskov, G. W. DeBell, Application of the needle optimization technique to the design of optical coatings, Appl. Opt. 35, 5493-5508 (1996).

**[2]** S. Larouche, L. Martinu, OpenFilters: open-source software for the design, optimization, and synthesis of optical filters, Appl. Opt. 47, C219-C230 (2008).

**[3]** M. Trubetskov, Deep search methods for multilayer coating design, 59, A75-A82 (2020).

**[4]** A. Moroz, A recursive transfer-matrix solution for a dipole radiating inside and outside a stratified sphere, Ann. Phys. 315, 352-418 (2005).

**[5]** I. Rasskazov, P. Carney, A. Moroz, STRATIFY: a comprehensive and versatile MATLAB code for a multilayered sphere, OSA Contin. 3, 2290 (2020).

# Requirements

- NumPy

- SciPy

- Numba

- mpi4py

# Installation

```
pip install eschallot
```

# Tutorial

1. [Example 1-1](./runfiles/run_topology_optimization_mse_Qsca.py): Optimization of the Scattering Cross Section Spectrum

```python
import os
directory = os.path.dirname(os.path.realpath(__file__))

import numpy as np
from scipy.ndimage import gaussian_filter1d
import Eschallot.optimization.topology_optimization as topopt
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD

import warnings
warnings.filterwarnings('ignore')

# Materials
mat_profile = np.array(['Air','TiO2_Sarkar']) # Outer(including embedding medium) to inner
mat_needle = np.array(['SiO2_bulk','TiO2_Sarkar']) # 'TiO2_Sarkar','Au_JC','Si_Schinke','Ag_palik', etc.

# Wavelength & angle ranges over which the cost function is defined
lam_cost = np.linspace(400, 550, 16)
theta_cost = np.linspace(0, 180, 2)*np.pi/180 # 0: forward, 180: backward
phi_cost = np.array([0,90])*np.pi/180

# Wavelength & angle ranges over which to compute the final efficiencies and phase function
lam_plot = np.linspace(400, 550, 301)
theta_plot = np.linspace(0, 180, 2)*np.pi/180 # 0: forward, 180: backward
phi_plot = np.array([0,90])*np.pi/180
```

* Materials
  - All materials are specified using the name of the corresponding text file containing the refractive index spectrum. The list of all materials available by default may be found [here](./eschallot/material_data). The user can also set up a separate directory for their own material data which can be provided as a parameter to the optimizer (explained in more detail below).
  - **mat_profile**: specifies the materials in the following order -> embedding medium > outermost shell > n-th shell > core
  - **mat_needle**: specifies the materials that may be used as layers for the multi-shell particle. Order does not matter.
  - Note that it is recommended to initialize the optimization with a single-layer homogeneous particle (TiO2 in the above example).

* Wavelengths & Angles
  - **lam_cost**: defines the wavelength points that are used to define the cost function
  - **lam_plot**: defines the wavelength points over which the far field quantities are computed for the final output
  - Having a coarser sampling grid for **lam_cost** is beneficial for reducing computation cost. The same holds for the angle sampling. In this case, the cost function only depends on the scattering efficiency spectrum, so the angles are sampled minimally.

* Unit Conventions
  - Wavelength: nm
  - Angle: rad
  - Radius: nm

```python
class cost_obj:
    def __init__(self, Q_sca_tgt):
        self.Q_sca_tgt = Q_sca_tgt
    
    def cost(self, Q_sca, Q_abs, Q_ext, p, diff_CS, t_El, t_Ml):
        cost = np.mean((Q_sca - self.Q_sca_tgt)**2)
    
        return cost
    
    def gradient(self, Q_sca, Q_abs, Q_ext, p, diff_CS, t_El, t_Ml, dQ_sca, dQ_abs, dQ_ext, dp, d_diff_CS, dt_El, dt_Ml, r):
        jac = np.mean(2*(Q_sca - self.Q_sca_tgt)[:,np.newaxis]*dQ_sca, axis=0)
    
        return jac

# Define Cost Function
n_seed = 0
np.random.seed(n_seed)
Q_sca_tgt = gaussian_filter1d(np.random.rand(39), 3)
Q_sca_tgt = 2*(Q_sca_tgt - np.min(Q_sca_tgt))/np.ptp(Q_sca_tgt)
Q_sca_tgt = Q_sca_tgt[12:28]

np.savez(directory + '/mse_Q_sca_tgt_seed' + str(n_seed), Q_sca_tgt=Q_sca_tgt)

custom_cost = cost_obj(Q_sca_tgt=Q_sca_tgt)
```

* Cost Function
  - The cost function has the following requirements:
    - It must be a defined as a Python class with methods **cost** and **gradient**
    - The **cost** method must take arguments **Q_sca, Q_abs, Q_ext, p, diff_CS, t_El, t_Ml** (even if not all are used in the computation of the cost) and output a scalar
    - The **gradient** method must take arguments **Q_sca, Q_abs, Q_ext, p, diff_CS, t_El, t_Ml, dQ_sca, dQ_abs, dQ_ext, dp, d_diff_CS, dt_El, dt_Ml, r** and output a 1D array or a scalar (when **N_params** == 1)
  - **dQ_sca, dQ_abs**, etc. indicate the derivatives of **Q_sca, Q_abs**, etc. with respect to the radial positions of layer interfaces, which are computed internally and provided as parameters. The user must provide the code for the gradient of the cost function with respect to the radial positions in terms of **dQ_sca, dQ_abs**, etc.
  - The arguments for **cost** and **gradient** have the following indexing convention:
    - **Q_sca, Q_abs, Q_ext**: (wavelength)
    - **p, diff_CS**: (wavelength, theta, phi)
    - **t_El, t_Ml**: (wavelength, order)
    - **dQ_sca, dQ_abs, dQ_ext**: (wavelength, layer interfaces)
    - **dp, d_diff_CS**: (wavelength, theta, phi, layer interfaces)
    - **dt_El, dt_Ml**: (wavelength, order, layer interfaces)
    - **r**: (layer interfaces)

```python
# Sweep Settings
r_min = 10
r_max = 1000
N_sweep = int(r_max - r_min) + 1
d_low = 5
max_layers = None

if 'Ag_palik' in mat_needle:
    output_filename = directory + '/topopt_result_mse_Qsca_lossy_' + str(mat_profile[1]) + '_rmax' + str(r_max) + '_seed' + str(n_seed)
else:
    output_filename = directory + '/topopt_result_mse_Qsca_lossless_' + str(mat_profile[1]) + '_rmax' + str(r_max) + '_seed' + str(n_seed)

t1 = time.time()
topopt.radius_sweep(output_filename,
                    r_min,
                    r_max,
                    N_sweep,
                    d_low,
                    max_layers,
                    mat_profile,
                    mat_needle,
                    lam_cost,
                    theta_cost,
                    phi_cost,
                    lam_plot,
                    theta_plot,
                    phi_plot,
                    custom_cost,
                    mat_data_dir=None,
                    lmax=None,
                    N_final=10,
                    verbose=0,
                    )
t2 = time.time()

max_mem_kb_proc = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
max_mem_kb = comm.reduce(max_mem_kb_proc, op=MPI.SUM, root=0)

if comm.rank == 0:
    print('### Time Elapsed: ' + str(np.round(t2 - t1, 3)) + ' s', flush=True)
    print('### Maximum Memory Usage: ' +str(np.round(max_mem_kb/1024**2, 3)) + ' GB', flush=True)
```

* Radius Sweep Settings
  - Since the shape optimization subroutine uses gradient descent, the final optimized design depends heavily on the initial parameters. Therefore, the algorithm optimizes multiple particles with different radii in parallel. A total of **N_sweep** particles are optimized that have initial radii between **r_min** and **r_max** with equal incrementation.
  - After an initial shape optimization step, multiple particles can converge to the same radii. These redundant particles are removed before the algorithm proceeds with the full topology optimization of all remaining candidates.
  - **d_low**: minimum layer thickness allowed in the final design
  - **max_layers**: maximum number of layers allowed in the final design

* Quality of Life Features
  - **r_min** and **r_max** are used as the minimum and maximum overall radii for the final designs.
  - A custom material directory may be passed to the optimizer using the **mat_data_dir** parameter.
  - **lmax** specifies the maximum order of the multipoles used in the Mie scattering computation (can be used to reduce computation cost at the expense of accuracy).
  - The top **N_final** designs are saved into an .npz file (adjust if output file is too large).
  - **verbose** (*note*: use single-processing when **verbose** > 0 for better readability):
    - 0: only prints optimization progress information
    - 1: additionally prints design parameters at every iteration
    - 2: additionally prints topology nucleation details
    - 3: enables verbose outputs from the **minimize** and **minimize_scalar** solvers from **scipy.optimize**.

```python
import os
directory = os.path.dirname(os.path.realpath(__file__))

import numpy as np
import eschallot.mie.simulate_particle as sim
import eschallot.util.read_mat_data as rmd

import warnings
warnings.filterwarnings('ignore')

# Wavelength & angle ranges over which to compute the final efficiencies and phase function
lam_plot = np.linspace(400, 550, 301)
theta_plot = np.linspace(0, 180, 2)*np.pi/180 # 0: forward, 180: backward
phi_plot = np.array([0,90])*np.pi/180

identifier = 'mse_Qsca_lossy_TiO2_Sarkar_rmax1000_seed0'

with np.load(directory + '/topopt_result_' + identifier + '.npz') as data:
    idx = 0
    N_layer = data['N_layer'][idx]
    r = data['r'][idx,:int(N_layer)]
    
    # Create n
    mat_profile = np.array(['Air','Ag_palik','SiO2_bulk','Ag_palik','TiO2_Sarkar'])
    mat_type = list(set(mat_profile))
    raw_wavelength, mat_dict_plot = rmd.load_all(lam_plot, 'n_k', mat_type)
    
    n = np.zeros((np.size(lam_plot,0), np.size(mat_profile,0))).astype(complex)
    count = 0
    for mat in mat_profile:
        n[:,count] = mat_dict_plot[mat]
        count += 1

Q_sca, Q_abs, Q_ext, p, diff_CS, t_El, t_Ml, Q_sca_mpE, Q_sca_mpM,\
    S1_mpE, S1_mpM, S2_mpE, S2_mpM = sim.simulate(lam_plot, theta_plot, phi_plot, r, n)
```

* [Example 1-2](./runfiles/run_analysis_mse_Qsca.py): Multipole Analysis
  - Multipole decomposition of optimized results can be done using **eschallot.mie.simulate_particle.simulate**
  - Output variables:
    - **Q_sca, Q_abs, Q_ext**: scattering, absorption, and extinction cross sections
    - **p, diff_CS**: scattering phase function and differential cross section
    - **t_El, t_Ml**: electric and magnetic Mie coefficients
    - **Q_sca_mpE, Q_sca_mpM**: scattering cross sections of each multipole mode (Eq. (27) in [ref.](https://doi.org/10.1016/j.cpc.2025.109966))
    - **S1_mpE, S1_mpM, S2_mpE, S2_mpM**: complex scattering amplitudes of each multipole mode (function of wavelength and angle) (Eq. (8) in [ref.](https://doi.org/10.1016/j.cpc.2025.109966))

* Optimization Results

![](ex1_fig1.png)

2. [Example 2](./runfiles/run_topology_optimization_linAttCoeff.py): Optimization of a Particle with High Linear Attenuation Coefficient



2. [Example 2](./runfiles/run_topology_optimization_directional_scatterer.py): Optimization of a Directional Scatterer

```python
class directional_reflector_cost:
    def __init__(self, ind_th_fwd, ind_th0, ind_th1, ind_phi_tgt, ind_wvl_tgt, theta):
        self.ind_th_fwd = ind_th_fwd
        self.ind_th0 = ind_th0
        self.ind_th1 = ind_th1
        self.ind_phi_tgt = ind_phi_tgt
        self.ind_wvl_tgt = ind_wvl_tgt
        self.theta = theta
        self.N_phi = ind_phi_tgt.size
    
    def cost(self, Q_sca, Q_abs, Q_ext, p, diff_CS):
        res = 0
        for i in range(self.N_phi):
            numer = np.sum(p[self.ind_wvl_tgt,self.ind_th0:self.ind_th1,self.ind_phi_tgt[i]]*np.sin(self.theta[self.ind_th0:self.ind_th1])[np.newaxis,:], axis=1)
            denom = np.sum(p[self.ind_wvl_tgt,self.ind_th_fwd:,:]*np.sin(self.theta[self.ind_th_fwd:])[np.newaxis,:,np.newaxis], axis=(1,2))
            res += -numer/denom
        
        return res
    
    def gradient(self, Q_sca, Q_abs, Q_ext, p, diff_CS, dQ_sca, dQ_abs, dQ_ext, dp, d_diff_CS, r):
        N_params = dQ_sca.shape[1]
    
        jac = np.zeros(N_params)
        for l in range(N_params):
            denom = np.sum(p[self.ind_wvl_tgt,self.ind_th_fwd:,:]*np.sin(self.theta[self.ind_th_fwd:])[np.newaxis,:,np.newaxis], axis=(1,2))
            d_denom = -np.sum(dp[self.ind_wvl_tgt,self.ind_th_fwd:,:,l]*np.sin(self.theta[self.ind_th_fwd:])[np.newaxis,:,np.newaxis], axis=(1,2))/denom**2
            for i in range(self.N_phi):
                numer = np.sum(p[self.ind_wvl_tgt,self.ind_th0:self.ind_th1,self.ind_phi_tgt[i]]*np.sin(self.theta[self.ind_th0:self.ind_th1])[np.newaxis,:], axis=1)
                d_numer = np.sum(dp[self.ind_wvl_tgt,self.ind_th0:self.ind_th1,self.ind_phi_tgt[i],l]*np.sin(self.theta[self.ind_th0:self.ind_th1])[np.newaxis,:], axis=1)
                
                jac[l] += -(d_numer/denom + numer*d_denom)
        
        return np.squeeze(jac)

# Define Cost Function
custom_cost = directional_reflector_cost(ind_th_fwd=11, # 5.5 deg (exclusive)
                                         ind_th0=291, # 145.5 deg (inclusive)
                                         ind_th1=302, # 151 deg (exclusive)
                                         ind_phi_tgt=np.array([0]), # 0 deg
                                         ind_wvl_tgt=0, # 450 nm
                                         theta=theta_cost,
                                         N_phi=phi_cost.size)
```

* Cost Function
  - The amount of scattering towards a given direction in spherical coordinates can be computed as the integral of sin(theta)*p(theta, phi) over the angular axes. The cost is similarly defined as the integral of the phase function over the target angles divided by the integral of the phase function over all angles, both integrals weighted by sin(theta).
  - **ind_th_fwd**: the forward scattering phase function is related to the total scattering cross section by the optical theorem. Restricting forward scattering tends to lead to particles with smaller size parameters that does not support enough multipole modes to achieve complex angular phase functions. Therefore, only angles above **theta[ind_th_fwd]** are included in the cost function.
  - **ind_th0, ind_th1**: indices that mark the target angle range
  - **ind_phi_tgt**: a numpy array of target azimuthal angles
  - **ind_wvl_tgt**: target wavelength index
  - **theta**: polar angle sampling grid
  - In the above example, the target angles are theta = 148 deg (with a 2.5 deg margin on either side) and phi = 0 deg

![](ex2_fig1.png)

3. [Example 3](./runfiles/run_monte_carlo_mse_Qsca.py): Simulation of Particle-Dispersed Random Media 1

   - In this example, we simulate the R, T, A spectra of a particle-dispersed medium where the optimized particle from Example 1 is used as the embedded particle.

```python
import os
directory = os.path.dirname(os.path.realpath(__file__))

import numpy as np
import Eschallot.mie.simulate_particle as sim
import Eschallot.util.read_mat_data as rmd
import Eschallot.montecarlo.monte_carlo_BSDF as mc
import time
import subprocess
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
status = MPI.Status()

# Simulation Settings
pht_per_wvl = 1e5 # number of photons (on average) to simulate for each sampled wavelength
lam_step = 10 # wavelength sampling step size (in nm)
lam1 = 400 # wavelength start (nm)
lam2 = 550 # wavelength end (nm)
polarization = 'random' # 'random', 'x', or 'y'

wvl = int((lam2 - lam1)/lam_step) + 1
wavelength = np.linspace(lam1, lam2, wvl, endpoint=True)
n_photon = wvl*pht_per_wvl

antireflective = 0 # assume antireflective coating on the top surface
Lambertian_sub = 0 # assume the substrate is a Lambertian scatterer
perfect_absorber = 0 # assume the substrate is a perfect absorber

output_filename = 'mse_Qsca'
subgroup = 32 # head + procs (total number of cores allocated for this job must be a multiple of this number)

N_theta_BSDF = 2
N_phi_BSDF = 2
init_theta = 0*np.pi/180
init_phi = 0*np.pi/180

# Film Configuration
config_layer = np.array(['Air','PMMA','Air']) # from top(incident side) to bottom(exit side), including background media
layer_thickness = 100e3 # thickness of the particle-dispersed layer (nm)
f_vol = 0.1 # particle volume fraction
```

* Simulation Settings
  - **subgroup**: the Monte Carlo simulator divides the available processes into subgroups. The **subgroup** parameter sets the number of processes per subgroup. Each subgroup is organized into a hierarchical structure where one head process assigns single-photon simulation jobs to worker processes and subsequently collects the results in an asynchronous manner (whenever each worker finishes its job). With smaller subgroups, the simulation speed is limited by the time taken by each worker to finish their jobs, whereas with larger subgroups, the simulation speed is limited by the communication between the head and worker processes. The optimal **subgroup** depends on how strongly the particle-dispersed medium scatters and also on the MPI and CPU specifications. The table below displays simulation times for this example for different subgroup configurations.

| Number of Subgroups | Procs per Subgroup | Total Number of Procs | Total Number of Worker Procs | Simulation Time (min) |
| -------------------:| ------------------:| ---------------------:| ----------------------------:| ---------------------:|
| 16 | 4 | 64 | 48 | 25.78 |
| 8 | 8 | 64 | 56 | 22.57 |
| 4 | 16 | 64 | 60 | 21.35 |
| 2 | 32 | 64 | 62 | 20.97 |
| 1 | 64 | 64 | 63 | 21.35 |

  - **N_theta_BSDF**: the polar angle sampling number for BSDF computation. In this example, the objective is the simulate the R, T, and A spectra only (without angular dependence data), so the parameter is set to 2 for minimal sampling.
  - **N_phi_BSDF**: the azimuthal angle sampling number of BSDF computation.
  - **init_theta**: the polar angle of incidence for incoming photons
  - **init_phi**: the azimuthal angle of incidence for incoming photons
  - **f_vol**: the particle volume fraction. Note that this Monte Carlo photon transport implementation assumes independent scattering, ***which is only valid for f_vol <= 0.1 in general***.

```python
# Define Phase Function Computation Grid
nu = np.linspace(0, 1, 501) # for even area spacing along theta
theta_pf = np.flip(np.arccos(2*nu[1:-1]-1))
phi_pf = np.linspace(0, 2*np.pi, 180, endpoint=False)

# Set (or load) Particle Geometry
config = np.array(['SiO2_bulk','TiO2_Sarkar']*6) # from out to in
r_profile = np.array([1000,
                      905.029,
                      887.905,
                      769.55,
                      751.257,
                      663.287,
                      367.799,
                      313.587,
                      276.148,
                      202.301,
                      150.519,
                      69.3268])

density = f_vol/((4*np.pi*r_profile[0]**3)/3)

# Compute Mie Scattering Quantities
mat_profile = np.hstack((config_layer[1], config))
mat_type = list(set(mat_profile))
mat_data_dir = None

raw_wavelength, mat_dict_default = rmd.load_all(wavelength, 'n_k', mat_type)
if mat_data_dir is not None:
    raw_wavelength, mat_dict_custom = rmd.load_all(wavelength, 'n_k', mat_type, directory=mat_data_dir)
else:
    mat_dict_custom = dict()
mat_dict = {**mat_dict_default, **mat_dict_custom}
    
n = np.zeros((wvl, mat_profile.size)).astype(complex)
count = 0
for mat in mat_profile:
    n[:,count] = mat_dict[mat]
    count += 1

Qs, Qa, Qe, pf, diff_CS, t_El, t_Ml, Q_sca_mpE, Q_sca_mpM,\
    S1_mpE, S1_mpM, S2_mpE, S2_mpM = sim.simulate(wavelength, theta_pf, phi_pf, r_profile, n)
Qa[Qa < 0] = 0
phase_fct = np.zeros((2, wvl, theta_pf.size, phi_pf.size))
phase_fct[0,:,:,:] = pf.copy()
phase_fct[1,:,:,:] = np.roll(pf, int(phi_pf.size/4), axis=2)
    
C_sca = (np.pi*r_profile[0]**2*Qs).flatten()
C_abs = (np.pi*r_profile[0]**2*Qa).flatten()

if rank == 0:
    if not os.path.isdir(directory + '/data'):
        os.mkdir(directory + '/data')
    np.savez(directory + '/data/Mie_data_' + output_filename, C_sca=C_sca, C_abs=C_abs, phase_fct=phase_fct)
```

* Angle Grid
  - The phase function is sampled in equal *solid angle* increments. The azimuthal angles can be sampled evenly, but the polar angle needs to be sampled sparsely near the poles and densely near the equator. This may be done by sampling a parameter **nu** (0 <= **nu** <= 1) evenly and converting to theta by arccos(2*nu - 1) (source: [Wolfram MathWorld](https://mathworld.wolfram.com/SpherePointPicking.html))

* Particle Geometry
  - **config**: an array of strings that define the material for each layer of the multi-shell particle from the shell to the core.
  - **r_profile**: the radial positions of the layer interfaces of the multi-shell particle from the outermost to the innermost interface.
  - The **Eschallot.mie.simulate_particle** module provides a function for computing the far-field quantities, Mie coefficients, and the scattering matrix elements of user-defined particles.
  - Specify a custom material data directory using **mat_data_dir** if needed.

```python
# Sync All Processes
comm.Barrier()

# Run the Monte Carlo Simulation
simulation = mc.monte_carlo(wavelength,
                            theta_pf,
                            phi_pf,
                            N_theta_BSDF,
                            N_phi_BSDF,
                            layer_thickness,
                            config_layer,
                            density,
                            C_sca,
                            C_abs,
                            phase_fct,
                            antireflective=antireflective,
                            Lambertian_sub=Lambertian_sub,
                            perfect_absorber=perfect_absorber,
                            init_theta=init_theta,
                            init_phi=init_phi,
                            polarization=polarization,
                            mat_data_dir=mat_data_dir,
                            )

t1 = time.time()
simulation.run_simulation(directory, comm, size, rank, status, n_photon, output_filename, subgroup)
t2 = time.time()
if rank == 0:
    print('Simlation Time: ' + str(t2 - t1) + ' s', flush=True)

    simulation.compute_BSDF(directory, size, output_filename, subgroup)
```

* Running the Simulation
  - The **run_simulation** method carries out the photon transport simulations.
  - The **compute_BSDF** method is only executed by one process which collects raw data from the head processes of each subgroup and computes the BSDF, R, T, A, and other relevant quantities.
  - The plots below may be found in the ./plot directory that will be created when the simulation runs (note that the data in these plots are only from one simulation subgroup, so the overall data will have less noise when summed over all subgroups).

![](ex3_fig1.png)

4. [Example 4](./runfiles/run_monte_carlo_directional_reflector.py): Simulation of Particle-Dispersed Random Media 2

   - In this example, we simulate the BSDF of a particle-dispersed medium where the optimized particle from Example 2 is used as the embedded particle.
  
```python
# Simulation Settings
pht_per_wvl = 5e6 # number of photons (on average) to simulate for each sampled wavelength
lam_step = 10 # wavelength sampling step size (in nm)
lam1 = 450 # wavelength start (nm)
lam2 = 450 # wavelength end (nm)
polarization = 'x' # 'random', 'x', or 'y'

wvl = int((lam2 - lam1)/lam_step) + 1
wavelength = np.linspace(lam1, lam2, wvl, endpoint=True)
n_photon = wvl*pht_per_wvl

antireflective = 0 # assume antireflective coating on the top surface
Lambertian_sub = 0 # assume the substrate is a Lambertian scatterer
perfect_absorber = 0 # assume the substrate is a perfect absorber

wvl_for_polar_plots = np.array([450]) # wavelengths at which the polar reflection/transmission plots are drawn

output_filename = 'directional_reflector'
subgroup = 32 # head + procs (total number of cores allocated for this job must be a multiple of this number)

N_theta_BSDF = 121
N_phi_BSDF = 18
init_theta = 0*np.pi/180
init_phi = 0*np.pi/180

# Film Configuration
config_layer = np.array(['Air','PMMA','Air']) # from top(incident side) to bottom(exit side), including background media
layer_thickness = 100e3 # thickness of the particle-dispersed layer (nm)
f_vol = 0.05 # particle volume fraction
```

* Simulation Settings
  - Compared to Example 3, here we:
    - only run the simulation at a single wavelength, but with increased angular resolution for the BSDF, which necessitates the simulation of an increased number of photons per wavelength.
    - have x-polarized incident photons, which will result in two reflection peaks at phi = 0 deg and phi = 180 deg in the diffuse angular BRDF plot. These peaks are due to single-scattered photons that are scattered at a polar angle near 148 deg by the embedded particles (as was optimized in Example 2).
  
| Number of Subgroups | Procs per Subgroup | Total Number of Procs | Total Number of Worker Procs | Simulation Time (min) |
| -------------------:| ------------------:| ---------------------:| ----------------------------:| ---------------------:|
| 16 | 4 | 64 | 48 | 26.03 |
| 8 | 8 | 64 | 56 | 22.63 |
| 4 | 16 | 64 | 60 | 21.30 |
| 2 | 32 | 64 | 62 | 20.88 |
| 1 | 64 | 64 | 63 | 21.98 |
  
![](ex4_fig1.png)