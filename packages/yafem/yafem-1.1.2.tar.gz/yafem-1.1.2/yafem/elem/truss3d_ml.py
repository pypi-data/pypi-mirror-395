import numpy as np
from yafem.elem.core_elem import core_elem
from yafem.elem.truss3d_ml_func import *

class truss3d_ml(core_elem):
    """
    my_nodes : nodes
        Node container providing coordinates and connectivity.

    pars : dictionary
        E            : float,   Young's modulus of the truss (default 2.10e11)
        D            : float,   Diameter of the truss/cable (default 0.1 m)
        A            : float,   Cross-sectional area (default 0.25 * pi * D^2)
        rho_m        : float,   Material density (default 7850 kg/m3)
        rho_w        : float,   Water density (default 1025 kg/m3)
        g            : float,   Gravity acceleration (default 9.82 m/s2)
        eG_pre       : float,   Prestressing strain (default 0.0)
        ub           : array,   Body displacement (default zeros)
        vb           : array,   Body velocity (default zeros)
        ab           : array,   Body acceleration (default zeros)
        uw           : array,   Water displacement (default zeros)
        vw           : array,   Water velocity (default 1e-3 ones)
        aw           : array,   Water acceleration (default zeros)
        cM           : float,   Added mass coefficient (default 1.0)
        cD           : float,   Non-linear drag coefficient (default 1.0)
        cV           : float,   Linear drag coefficient (default 1.0)
        cF           : float,   Friction coefficient (default 1.0)
        cL           : float,   Lift coefficient (default 1.0)
        time_modu_w  : function, Time modulation function for water (default lambda t: 1 - exp(-t/5))
        time_modu_g  : function, Time modulation function for gravity/prestress (default lambda t: 1 - exp(-t/5))
        nodal_labels : list[int], Node connectivity (default [1, 2])
    """
    #%% class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        self.linear_M = True
        self.linear_K = True
        self.linear_C = True

        # extract parameters and assign default values
        self.__extract_pars(pars)

        # set the number of dofs per node
        self.__element_dofs(3)

        # Coordinate transformation matrix calculation
        r = self.nodal_coords[1] - self.nodal_coords[0]
        r /= np.linalg.norm(r)
        
        # Determine a perpendicular vector s and orthogonalize
        s = np.array([0.0, 1.0, 0.0]) if r[2] != 0 else np.array([-r[1], r[0], 0.0])
        s -= np.dot(s, r) * r
        s /= np.linalg.norm(s)

        # Compute t as the orthogonal cross product
        t = np.cross(r, s)
        t /= np.linalg.norm(t)

        # Create transformation matrix
        self.T = np.array([r, s, t])
        
        self.G = np.zeros((6, 6))
        self.G[0:3, 0:3] = self.T
        self.G[3:6, 3:6] = self.T
       
        # nodal coordinates flattend
        n_coord_flattend = self.nodal_coords.flatten()

        i = 0.000001

        # parameters
        params_fg = [self.rho_w, 
                     self.rho_m, 
                     self.g * self.time_modu_g(i), 
                     self.A, 
                     self.D,
                     self.L]
        
        # coefficients
        coef = [self.cM, 
                self.cD, 
                self.cV, 
                self.cF, 
                self.cL]
        
        # flattend displacement anf velocity
        u_flattend  = self.u.flatten()
        v_flattend  = self.v.flatten()
        uw_flattend = self.uw.flatten()
        vw_flattend = self.vw.flatten()

        # combined variables
        vars = [u_flattend,
                v_flattend,
                uw_flattend * self.time_modu_w(i),
                vw_flattend * self.time_modu_w(i),
                params_fg,
                coef,
                n_coord_flattend]

        #%% Mechanical

        # relative nodal coordinated (deformed configuration)
        self.xk = (self.nodal_coords[1,:] - self.nodal_coords[0,:]) + \
                  (self.u[3:6] - self.u[0:3])
        
        # length of the element (deformed)
        self.Lk = np.linalg.norm(self.xk)
        
        # Green-Lagrange strain (deformed)
        self.eG = (self.Lk**2 - self.L**2) / (2 * self.L**2) + \
                  self.eG_pre * self.time_modu_g(i) # (1-np.exp(-t/self._tau)) # pre-stressing is ramped
        
        # update of the axial force
        self.N = self.A * self.E * self.eG
        # N_pre_tension = self.A * self.E * self.eG_pre * self.time_modu_g(i) # (1-np.exp(-t/self._tau)) # pre-stressing is ramped

        self.fg = truss3d_ml_fg(params_fg,n_coord_flattend).squeeze()
        self.s_tension = self.N / self.L * np.hstack((-self.xk, self.xk)) 

        # mechanical restoring force
        self.r_mec = self.s_tension + self.fg

        # Identity matrix
        I = np.eye((3))
        xk_outer = np.outer(self.xk, self.xk)

        # mechanical tangent stiffness
        self.K_mec = ((self.E * self.A) / self.L**3) * np.block([[ xk_outer, -xk_outer],
                                                                 [-xk_outer,  xk_outer]]) + \
                     (self.N / self.L) * np.block([[ I, -I],
                                                   [-I,  I]])
        
        # mechanical mass matrix
        self.M_mec = (self.A * self.L * self.rho_m * 0.5) * np.eye(6)

        # damping matrix in global coordinates
        # self.C = np.zeros_like(self.K_mec)

        #%% Hydrodynamical

        # hydrodynamic force vector, stiffness matrix and damping matrix
        self.r_hyd = truss3d_ml_r_hyd(*vars).squeeze()
        self.K_hyd = truss3d_ml_K_hyd(*vars) 
        self.C_hyd = truss3d_ml_C_hyd(*vars)

        #%% Global reference
        self.r = self.r_mec + self.r_hyd
        self.K = self.K_mec + self.K_hyd
        self.C =              self.C_hyd
        self.M = self.G.T @ self.M_mec @ self.G

        # # Stiffness matrix in global coordinate system
        # self.K = self.G.T @ self.Kl @ self.G
        # self.M = self.G.T @ self.Ml @ self.G

        # # damping matrix in global coordinates
        # self.C = np.zeros_like(self.K)

        # # strain interpolation matrix in global coordinates
        # self.B = self.Bl @ self.G

        # # displacement interpolation matrix in global coordinates
        # self.N = self.Nl @ self.G

        # # local to global coordinate transformation
        # self.r = self.G.T @ self.rl     
 
    #%% extract parameters
    def __extract_pars(self, pars):
        
        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'beam3d_ml'

        # mechanical parameters
        self.eG_pre = pars.get('eG_pre',0.0) # prestressing strain [Pa]
        self.E = pars.get("E", 2.10e11) # Youngs modulus
        self.D = pars.get('D',0.1) # cable diameter [m]
        self.A = pars.get('A',0.25 * np.pi * self.D**2) # cross-sectional area

        # mass parameters
        self.rho_m = pars.get('rho_m',7850.0) # cable material density [kg/m3]
        self.rho_w = pars.get('rho_w',1025.0) # water density [kg/m3]
        self.g     = pars.get('g',9.82) # gravity acceleration [m/s2]

        # body kinematics
        self.ub = pars.get('ub', np.zeros((6)))  # body displacement (not relevant)
        self.vb = pars.get('vb', np.zeros((6)))  # body velocity [m/s]
        self.ab = pars.get('ab', np.zeros((6)))  # body acceleration (not relevant)
        
        # water kinematics
        self.uw = pars.get('uw', np.zeros((6)))  # Water displacement (not relevant)
        self.vw = pars.get('vw', 1e-3 * np.ones((6)))  # Water velocity [m/s]
        self.aw = pars.get('aw', np.zeros((6)))  # Water acceleration (not relevant)
        
        # coefficients
        self.cM = pars.get('cM', 1.0) # [-] added mass coefficient
        self.cD = pars.get('cD', 1.0) # [-] non-linear drag coefficient
        self.cV = pars.get('cV', 1.0) # [m/s] linear drag coefficient
        self.cF = pars.get('cF', 1.0) # [-] friction coefficient
        self.cL = pars.get('cL', 1.0) # [-] lift coefficient

        # initialization of element vectors
        self.u = np.zeros((6))
        self.v = self.u.copy()
        self.a = self.u.copy()
        self.q = np.zeros((0))

        # Time modulation
        self.time_modu_w = pars.get("time_modu_w",lambda t: 1 - np.exp(-t/5.0)) # water velocity [m/s]
        self.time_modu_g = pars.get("time_modu_g",lambda t: 1 - np.exp(-t/5.0)) # water acceleration [m/s2]

        # self.alpha = pars.get("alpha", 0.0) # coefficient of thermal expansion 
        # self.theta = pars.get("theta", 0.0) # Thermal loading
        self.nodal_labels = pars.get("nodal_labels", [1, 2])
        
        # extract nodal coordinates
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels)
        self.L = np.linalg.norm(self.nodal_coords[1] - self.nodal_coords[0])
    
        # temperature controlled dofs
        # self.dofs_q = np.array(pars.get("dofs_q", []), dtype=np.int32).reshape(-1, 2) if "dofs_q" in pars else np.zeros((0, 2), dtype=np.int32)
    
    #%% Computing element dofs
    def __element_dofs(self, dofs_per_node):

        self.dofs = np.empty([dofs_per_node*2,2],dtype=int)

        self.dofs[0:dofs_per_node,0] = self.nodal_labels[0] # Label of first node
        self.dofs[dofs_per_node:,0]  = self.nodal_labels[1] # Label of second node
        self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 2) + 1 # Dofs of both nodes
    
        return self.dofs

    #%% Plot 3d elements
    def plot(self, ax, x=None, y=None, z=None, color='k-'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]

        # Collect lines
        lines = [[[x[0], y[0], z[0]],[x[1], y[1], z[1]]]]

        return lines, None
    
    def dump_to_paraview(self):
        # here it goes the dump_to_paraview implementation for the beam3d element
        pass
